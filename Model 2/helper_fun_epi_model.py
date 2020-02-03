## Help function for SIR 2019-nCoV estimation
## Author: Yran Jing
## Date: 2020-02-02

import numpy as np
import scipy.optimize as optimization
import pandas as pd
import pandas
from SIER_model import SIER

class Estimate_parameter:
    """
    Estimate other parameters: 
            beta in SIR model and R0(basic reproduction number)
    """
    def __init__(self, nu: float, k: int, t: np.ndarray, I: np.ndarray):
        self.nu = nu
        self.k = k # the number of people a confirmed case contacts daily
        self.t = t # time step
        self.I = I  # observation
        # Estimated beta
        self.beta = self._estimate_beta()
        # self.R0
        self.R0 = self._estimate_R0()
        
    def func(self, t: np.ndarray, b):
        """
        K is the mean number of people a confirmed case contacts daily
        """
        return np.exp((self.k*b-self.nu)*t)

    def _estimate_transmission_probablity(self):
        """
        Estimate the transmission probablity by non-linear OLS
        """
        return optimization.curve_fit(self.func, self.t, 
                                      self.I, maxfev=1000)[0][0]
    def _estimate_beta(self):
        """
        Estimate beta of SIR model
        """
        return self.k * self._estimate_transmission_probablity()
    
    def _estimate_R0(self):
        """
        Estimate R0(basic reproduction number)
        """
        return (self.beta)/self.nu
    
    def __str__(self): 
        """
        Representation
        """
        return f"""Estimate the transmission probablity: {round(self._estimate_transmission_probablity(), 2)} 
Estimated R0(basic reproduction number): {round(self.R0,1)}
"""



class Estimate_Wuhan_Outbreak(Estimate_parameter):
    
    def __init__(self, Est: Estimate_parameter, k: int, N: int,
                E0: int, I0: int, R0: int, T: int, econ: int):
        self.Est = Est 
        print(self.Est) # print R0 
        self.k = k # the number of people one case contacts daily, which nflunenced by government force
        self.N = N
        self.E0 = E0 # initial number of Enfective cases
        self.I0 = I0 # initial number of recovered cases
        self.R0 = R0
        self.S0 = N - E0 - I0 - R0# initial number of suspective cases
        self.alpha = 1/T # T is the mean of incubation period
        self.econ = econ
        self.model = None
        
        
    def _run_SIER(self,title:str, ylabel:str, xlabel:str, show_Sus = True) -> pandas.core.frame.DataFrame:
        """
        Run SIER model
        """
        Est_beta = self.Est._estimate_transmission_probablity()*self.k
        sier = SIER(eons=self.econ, Susceptible=self.N-self.E0-self.I0-self.R0, Exposed = self.E0, 
                    Infected=self.I0, Resistant=self.R0, rateSI=Est_beta, rateIR=self.Est.nu, 
                    rateAl = self.alpha)
        result = sier.run()
        # Draw plot
        if show_Sus:
            sier.plot(title, ylabel, xlabel)
        else:
            sier.plot_noSuscep(title, ylabel, xlabel)
        
        self.model = sier
        return result
        