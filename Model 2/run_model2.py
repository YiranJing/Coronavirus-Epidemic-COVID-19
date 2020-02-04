## Author: Yiran JIng
## Date: 04 Feb 2020

import numpy as np
import pandas as pd
import pandas
from SIER_model import SIER
from SIR_model import SIR
from matplotlib import pyplot as plt
from helper_fun_epi_model import *
import scipy.optimize as optimization
import warnings
warnings.filterwarnings('ignore')

"""
Data from Chinese Center for Disease Control and Prevention (DOC) 
"""
# 2019-12-08 is the first date, when find the first case. 
t = np.asarray([0, 42, 43, 44, 45, 46])  # time
I = np.asarray([1,198,218,320,478,639]) # number of official confirmed cases


def main():
    
    # estimate R0 and beta
    Est = Estimate_parameter(nu = 1/14, k = 5, t = t, I = I)
    print(Est)
    
    # run model before 23 Jan
    """
    Baseline: before 23 Jan 
    
    2019-12-08: 
    I0 = 1: 1confirmed cases
    E0 = 5: Based on the data in Early Transmission Dynamics report, there are 5 cases were confirmed 
    in the next 7 days after the first case. So E0 = 5. 
    R0 = 0: no people died or recover
    """
    print("\n\nBaseline before 23 Jan")
    baseline = Estimate_Wuhan_Outbreak(Est, k = 5, N=11000000,
                    E0 = 5, I0 = 1, R0 = 0, T=7, econ = 400)
    result = baseline._run_SIER('Estimated 2019-nCoV Outbreak in Wuhan Since 2019-12-08 without Government Control',
            'Wuhan Population (x 10 million)', 'Days after 2019-12-08', death_rate = 0.03)
    
    
    # run model after 23 
    """
    after Wuhan shut down (after 23 Jan)
    beta: The contact rate is half than before
    N = 9000000
    k = 1 # effective goverment control and individual protection
    
    2020 Feb 02:
    R0 = 175+224. curedCount: 175, deadCount: 224
    I0 = 4109 # offical number on 02 Feb
    
    Suppose E0 = I0*5: the number of ppl in incubation is 5 times the confirmed cases.
    """
    print("\n\nBaseline after 23 Jan")
    case1 = Estimate_Wuhan_Outbreak(Est, k = 1, N=9000000,
                    E0 = 4109 * 5, I0 = 4109, R0 = (175+224), T=7, econ = 120)
    result2 = case1._run_SIER('Forecat 2019-nCoV Outbreak in Wuhan after 2020-02-02 using offical number',
            'Wuhan Population','Days after 2020-02-02', death_rate = 0.03, show_Sus = False)
    
    
    #Sensitvity analysis
    """
    case 1:
    S0 using the estimated result from model 1
    There are 46000 cases in wuhan until 23 Jan:
       Assume the infected case are 20% only
       The lefs are in incubation period
    Assume the death rate = cure rate = 3% 
    """
    print("\n\ncase 1")
    N = 9000000
    I0 = 38500 *1/5
    E0 = 38500 * 4/5
    R0 = I0 * (0.03+0.03) # suppose the death rate is 3% (official), equal to cure rate
    k = 1
    # estimate beta and R0
    Est_beta = Est._estimate_transmission_probablity()*k
    
    case2 = Estimate_Wuhan_Outbreak(Est, k = 1, N=9000000,
                    E0 = E0, I0 = I0, R0 = R0, T=7, econ = 120)
    result3 = case2._run_SIER('Case 1: Forecat 2019-nCoV Outbreak in Wuhan after 2020-01-23 using estimated data',
            'Wuhan Population','Days after 2020-01-23', death_rate = 0.03, show_Sus = False)
    
    
    """
    case2: Assume the mean duration of the infection is 30 days
    """
    print("\n\nCase 2")
    Est = Estimate_parameter(nu = 1/20, k = 5, t = t, I = I)
    
    Est_beta = Est._estimate_transmission_probablity()*k
    
    case2 = Estimate_Wuhan_Outbreak(Est, k = 1, N=9000000,
                    E0 = 4109 * 5, I0 = 4109, R0 = (175+224), T=7, econ = 120)
    result3 = case2._run_SIER('Case 2: Forecat 2019-nCoV Outbreak in Wuhan after 2020-02-02 using offical number',
            'Wuhan Population','Days after 2020-02-02', show_Sus = False, death_rate = 0.03)
    
    
    
    """
    case3: Assume k = 2, rather than 1, 
             since some cases cannot be detected correctly or immediately, Also not perfect isolation
    """
    print("\n\nCase 3")
    Est = Estimate_parameter(nu = 1/20, k = 5, t = t, I = I)
    
    Est_beta = Est._estimate_transmission_probablity()*k
    
    case2 = Estimate_Wuhan_Outbreak(Est, k = 2, N=9000000,
                    E0 = 4109 * 5, I0 = 4109, R0 = (175+224), T=7, econ = 120)
    result3 = case2._run_SIER('Case 3: Forecat 2019-nCoV Outbreak in Wuhan after 2020-02-02 using offical number',
            'Wuhan Population','Days after 2020-02-02', show_Sus = False, death_rate = 0.03)
    
    
    
    """
    case4: case 1 + case 2
    """
    print('\n\nCase 4')
    Est = Estimate_parameter(nu = 1/20, k = 5, t = t, I = I)
    
    N = 9000000
    I0 = 38500 *1/5
    E0 = 38500 * 4/5
    R0 = I0 * (0.03+0.03) # suppose the death rate is 3% (official), equal to cure rate
    k = 1
    # estimate beta and R0
    Est_beta = Est._estimate_transmission_probablity()*k
    
    case2 = Estimate_Wuhan_Outbreak(Est, k = 1, N=9000000,
                    E0 = E0, I0 = I0, R0 = R0, T=7, econ = 120)
    result3 = case2._run_SIER('Case 4: Forecat 2019-nCoV Outbreak in Wuhan after 2020-01-23 using estimated data',
            'Wuhan Population','Days after 2020-01-23', show_Sus = False, death_rate = 0.03,)
    

    
    """
    case5: case 1 + case 2 + case 3
    """
    print('\n\nCase 5')
    Est = Estimate_parameter(nu = 1/20, k = 5, t = t, I = I)
    
    N = 9000000
    I0 = 38500 *1/5
    E0 = 38500 * 4/5
    R0 = I0 * (0.03+0.03) # suppose the death rate is 3% (official), equal to cure rate
    k = 1
    # estimate beta and R0
    Est_beta = Est._estimate_transmission_probablity()*k
    
    case2 = Estimate_Wuhan_Outbreak(Est, k = 2, N=9000000,
                    E0 = E0, I0 = I0, R0 = R0, T=7, econ = 120)
    result3 = case2._run_SIER('Case 5: Forecat 2019-nCoV Outbreak in Wuhan after 2020-01-23 using estimated data',
            'Wuhan Population','Days after 2020-01-23', show_Sus = False, death_rate = 0.03,)

    
                
if __name__ == '__main__':
    main()
