### Helper functions for model 1 
### Reference 
# https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf

## Author: Yiran Jing
## Date: Jan 2020
import numpy as np
from dataclasses import dataclass
from typing import List
from scipy.stats import nbinom, t
import matplotlib.pyplot as plt
from scipy import stats
import random
import math
from math import lgamma
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

def Binomial_log_like(n:int, p:float, k: int):
    """
    log-likelihood function of binomial distribution
    
    we use this function to calculate profile lihelihood 95% CI
    """
    loglik = lgamma(n+k+1) - lgamma(k+1) - lgamma(n+1) + k*np.log(p) + n*np.log(1-p)
    return loglik

class Wuhan:
    """
    Give the basic information of Wuhan, China
    """
    def __init__(self, population:int, airportCatchment:int, internationalTraveller: int):
        # Population of Wuhan
        self.population = population
        # Catchment population in Wuhan international airport 
        self.airportCatchment = airportCatchment
        # Total volume of international travel from Wuhan over last two month (Nov-Dec) per day
        self.internationalTraveller = internationalTraveller
        # Estimated daily probability of international travel
        self.internationalTravelPro = self._calculate_probability_internationalTravel()
    
    def _calculate_probability_internationalTravel(self):
        """
        daily probability of international travel = 
        daily outbound international traveller from Wuhan / catchment population of wuhan airport
        """
        return self.internationalTraveller/self.airportCatchment

class International:
    """
    Info of cases detected outside mainland China
    """
    def __init__(self, cases:int):
    # Number of cases detected outside mainland China
        self.cases = cases  
    
class Coronavirus:
    """
    Give the estimated information of Coronavirus
    """
    def __init__(self, incubation: int, onsetTodetection: int):
        # Estimated incubation period
        self.incubation = incubation
        # Estimated mean time from onset of symptoms to detection
        self.onsetTodetection = onsetTodetection
        # Estimated mean time to detection
        self.detection = self._calculate_detection()
    
    def _calculate_detection(self):
        """
        mean time to detection = incubation period + mean time from onset of symptoms to detection
        """
        return self.incubation + self.onsetTodetection
    
@dataclass    
class Estimate_wuhan_case:
    model_name: str
    date: str
    wuhan: Wuhan
    international: International
    coronavirus: Coronavirus
    
    def __str__(self): 
        """
        Representation
        """
        return f"""{self.date} 
Scenario: {self.model_name}
Exported number of confirmed cases: {self.international.cases}
Detection Window: {self.coronavirus.detection}
Time from onset of symptoms to detection: {self.coronavirus.onsetTodetection}
Daily International passengers travelling out of Wuhan: {self.wuhan.internationalTraveller}
Effective catchment population of Wuhan Interntional Airport: {self.wuhan.airportCatchment}

Estimated number of cases in Wuhan: {self.calculate_total_cases_inWuhan()}
Estimated 95% confidence interval: {self.calculate_conf_interval()}

------------------------------------------------------------------------------------
"""
    
    def calculate_total_cases_inWuhan(self):
        """
        total_cases_inWuhan = 
           number of cases detected overseas / probability anyone case will be detected overseas
        """
        p = self.calculate_pro_detected_overseas() # probability anyone case will be detected overseas
        return self.international.cases / p
    
    def calculate_pro_detected_overseas(self):
       """
       probability anyone case will be detected overseas = 
           daily probability of international travel * mean time to detection of a case
       """
       return self.wuhan.internationalTravelPro * self.coronavirus.detection
    
    def calculate_conf_interval(self, alpha=0.05):
        """
        Calculate confidence interval by profile likelihood method:
           Suppose population follows binomial distribution Bin(p,N)
           p: probability anyone case will be detected overseas
           n: negative binomially distributed function of X (number of cases detected outside mainland China)
        """
        k = self.international.cases
        p = self.calculate_pro_detected_overseas()
        n_est = self.calculate_total_cases_inWuhan()
        lb = math.inf; ub = -math.inf; # initialize the original lower bound and upper bound
        
        # search lb and ub
        for n in range(10, 100000, 10):
            LR = Binomial_log_like(n_est, p, k) - Binomial_log_like(n, p, k)
            if LR <1.92: # 95%-percentile of the Chi-square(1) distribution
                if n < lb: # the minimum value will be the lower bound
                    lb = n
                elif n> ub: # the max value is upper bound
                    ub = n  
        return (lb, ub)
        
    def plot_distribution(self):
        """
        Plot the distrubution of estimated Coronavirus cases in Wuhan 
        """
        p = self.calculate_pro_detected_overseas()
        n = self.international.cases
        
        fig, ax = plt.subplots(1, 1)
        x = np.arange(nbinom.ppf(0.025, n, p),
                   nbinom.ppf(0.975, n, p))
        ax.vlines(x, 0, nbinom.pmf(x, n, p), color='lightblue', lw=5, alpha=0.5)
        ax.set_title(" pmf of coronavirus cases in Wuhan " + self.date)

@dataclass
class Estimate_Period:
    collect: List[Estimate_wuhan_case] # collect time series
        
        
def sensitivity_analysis(date: str, wuhan_population: int,
                        airportCatchment: int, international_case: int, onsetTodetection: int,
                        incubation=6, internationalTraveller=3301):
    """
    Sensitivity analysis to estimate current cases in wuhan based on 3 scenario
    1. Baseline
    2. Smaller catchment:
        airportCatchment = wuhan_population
    3. Shorter detection window:
    """
    # scenario cases
    scenarios = ['Baseline', 'Smaller catchment', 'Shorter detection window']
    Catchment_old = airportCatchment
    onsetTodetection_old = onsetTodetection
    international_case_old = international_case
    
    for scenario in scenarios:
        if scenario == 'Smaller catchment':
            airportCatchment=wuhan_population
        elif scenario == 'Shorter detection window':
            onsetTodetection = 2
            
            
        wuhan_case = Estimate_wuhan_case(model_name = scenario, date = date, 
                                wuhan = Wuhan(population=wuhan_population, 
                                              airportCatchment=airportCatchment, 
                                              internationalTraveller=internationalTraveller),
                                international = International(cases = international_case),
                                coronavirus = Coronavirus(incubation=incubation, 
                                                          onsetTodetection=onsetTodetection))
        # plot                                                      
        # wuhan_case.plot_distribution()    
        
        # print model information
        print(wuhan_case)
        
        # convert to original 
        airportCatchment = Catchment_old
        onsetTodetection = onsetTodetection_old
        international_case = international_case_old  
        
        
        
        