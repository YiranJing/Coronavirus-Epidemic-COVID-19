## Author: Yiran Jing
## Date: 04 Feb 2020

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
from help_function_model1 import * 


def main():
    
    ## Baseline
    wuhan_case_Jan21 = Estimate_wuhan_case(model_name = 'Baseline', date = '2019-01-21', 
                                      wuhan = Wuhan(population=11000000, 
                                                    airportCatchment=19000000, 
                                                    internationalTraveller=3301),
                                      international = International(cases = 7),
                                      coronavirus = Coronavirus(incubation=6, 
                                                                onsetTodetection=4))

    print(wuhan_case_Jan21)
    # Plot the distrubution of estimated Coronavirus cases in Wuhan 
    wuhan_case_Jan21.plot_distribution()
    
    
    
    ## Sensitvty analysis
    # 2019-01-21: same result as papers 
    sensitivity_analysis(date='2019-01-21', wuhan_population=11000000,
                     airportCatchment=19000000,international_case=7, 
                     onsetTodetection=4)
    
    # 8 exported cases until Jan 22 
    sensitivity_analysis(date='2019-01-22', wuhan_population=11000000,
                        airportCatchment=19000000,international_case=8, onsetTodetection=4)
                
    # 2019-01-29: 67 confirmed cases overseas
    sensitivity_analysis(date='2019-01-29', wuhan_population=11000000,
                     airportCatchment=19000000,international_case=67, 
                     onsetTodetection=4)
        
               
                
if __name__ == '__main__':
    main()
