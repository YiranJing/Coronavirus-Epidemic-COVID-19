## Help function for SIR 2019-nCoV estimation
## Author: Yran Jing
## Date: 2020-02-02

import numpy as np
import scipy.optimize as optimization

class Estimate_parameter:
    """
    Estimate other parameters: 
            beta in SIR model and R0(basic reproduction number)
    """
    def __init__(self, nu: float, k: int, t: np.ndarray, I: np.ndarray):
        self.nu = nu
        self.k = k
        self.t = t
        self.I = I 
        # Estimated beta
        self.beta = self._estimate_beta()
        # self.R0
        self.R0 = self._estimate_R0()
        print()
        
    def func(self, t: np.ndarray, b):
        """
        K is the mean of the number of people a confirmed case contacts daily
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