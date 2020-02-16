## SEIR model
## Author: Yran Jing
## Date: 2020-02

import pandas as pd
import numpy as np
import operator
import matplotlib.pyplot as plt
import pandas as pd
import pandas
from math import *
import datetime
import matplotlib.dates as mdates
from helper_fun_epi_model import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
import warnings
warnings.filterwarnings('ignore')

class Train_Dynamic_SEIR:
    """
    'eons' (number of time points to model, default 1000)
    'Susceptible' (number of susceptible individuals at time 0, default 950)
    'Exposed' (number of individuals during incubation period)
    'Infected' (number of infected individuals at time 0, default 50)
    'Resistant' (number of resistant individuals at time 0, default 0)
    'rateSI' (base rate 'beta' from S to E, default 0.05)
    'rateIR' (base rate 'gamma' from I to R, default 0.01)
    'rateAl' (base rate of isolation 'altha', from E to I, default 0.1)
    """
    def __init__(self, data: pandas.core.frame.DataFrame, 
                 population: int, epoch = 1000, rateIR=0.01, rateAl = 0.1):
        self.epoch = epoch # change weights in each epoch
        self.steps = len(data) 
        # real observation
        self.Exposed = list(data['E'])
        self.Infected = list(data['I'])
        self.Resistant = list(data['R'])
        self.Susceptible = list(population - data['E'] - data['I'] - data['R'])
        # estimation
        self.S_pre = []; 
        self.E_pre = []; 
        self.I_pre = []; 
        self.R_pre = [];
        self.past_days = data['Days'].min() # count the number of days before the first traning point
        
        # other parameters within SEIR model
        self.c = 1; # intial guess
        self.b = -3; # intial guess
        self.alpha = 0.1; # intial guess
        self.rateSI = self._calculate_beta(c = self.c, t = 0, b = self.b, alpha = self.alpha) # intial guess
        self.rateIR = rateIR
        self.rateAl = rateAl
        self.numIndividuals = population # total population
        self.results = None
        self.estimation = None 
        self.modelRun = False
        self.loss = None
        self.betalist = []

    
    def _calculate_beta(self, c: float, t: int, alpha: float, b: float):
        """
        calculate beta based on some function
        """
        return c*exp(-alpha*(t+b))*pow((1 + exp(-alpha*(t+b))),-2)

    def _calculate_loss(self):
        """
        loss = sqrt (sum of squared loss)
        """
        return mean_squared_error(self.Infected, self.I_pre)
        
        
    def _calculate_MAPE(self):
        """
        Calcualte MAPE between estimated value and fitted value
        """
        y = np.array(self.Infected)
        y_pred = np.array(self.I_pre)
        mape = np.abs((y-y_pred))/np.abs(y)
        return np.mean(mape)
    
    def _calculate_MAPE_last_5_days(self):
        """
        Calcualte MAPE between estimated value and fitted value in the last 5 days, same as the test set of baseline
        """
        y = np.array(self.Infected[-5:])
        y_pred = np.array(self.I_pre[-5:])
        mape = np.abs((y-y_pred))/np.abs(y)
        return np.mean(mape)
    
    def _update(self):
        """
        try to find (global mini parameter)
        """
        E =  2.71828182846
        alpha_eta  = 0.000000000000001;
        b_eta = 0.00000000001;
        c_eta = 0.0000000000001;
        alpha_temp=0.0;
        c_temp=0.0;
        b_temp =0.0;
        for t in range(0, self.steps):
            
            formula1 = E**(-self.alpha*(t + self.b)) 
            formula2 = E**(self.rateSI*self.Susceptible[t]/self.numIndividuals - self.rateIR) * t
            formula3 = E**(self.alpha*(t + self.b)) 
            
            loss_to_beta = -2*(self.Infected[t] - self.I_pre[t])*(self.I_pre[t])*t*self.Susceptible[t]/self.numIndividuals
            
            #loss_to_beta = 2*(formula2 - self.Infected[t])*(formula2*self.Susceptible[t]*t)/self.numIndividuals
            
            # use chain rule to calculate partial derivative
            beta_to_alpha = -self.c*pow(formula1,2)*(t + self.b)*(formula3 -1)*pow((1+formula1),-3)
            beta_to_b = -self.c*pow(formula1,2)*self.alpha*(formula3 -1)*pow((1+formula1),-3)
            beta_to_c = formula1*pow((1+formula1),-2)
            
            alpha_temp += loss_to_beta * beta_to_alpha 
            b_temp += loss_to_beta * beta_to_b
            c_temp += loss_to_beta * beta_to_c
            
        
        self.alpha -= alpha_eta*alpha_temp; # update values
        self.b  -= b_eta*b_temp;
        self.c -= c_eta*c_temp;
     
        #print("c: {}, b: {}, alpha: {}".format(self.c, self.b, self.alpha))
     
    
    def train(self):
        """
        Use real-time data into SEIR model to do estimation
        Improve estimated parameter by epoch iteration
        Goal:
            find optimial beta(contact rate) by mini loss function
        """
        for e in range(self.epoch):
            # prediction list
            self.S_pre = []; self.E_pre = []; self.I_pre = []; self.R_pre = [];
            
            # make prediction step by step
            for t in range(0, self.steps):
                if t == 0:
                    self.S_pre.append(self.Susceptible[0])
                    self.E_pre.append(self.Exposed[0])
                    self.I_pre.append(self.Infected[0])
                    self.R_pre.append(self.Resistant[0])
                    
                    # collect the optimal fitted beta
                    if e == (self.epoch - 1):
                        self.rateSI = self._calculate_beta(c = self.c, t = t, b = self.b, 
                                                       alpha = self.alpha)
                        self.betalist.append(self.rateSI)
                
                else:
                    self.rateSI = self._calculate_beta(c = self.c, t = t, b = self.b, 
                                                       alpha = self.alpha)
                    #print(self.rateSI)
                    # collect the optimal fitted beta
                    if e == (self.epoch - 1):
                        self.betalist.append(self.rateSI)
                        
                    # apply real-time data into SEIR formula
                    S_to_E = (self.rateSI * self.Susceptible[t] * self.Infected[t]) / self.numIndividuals
                    E_to_I = (self.rateAl * self.Exposed[t])
                    I_to_R = (self.Infected[t] * self.rateIR)
                    self.S_pre.append(self.Susceptible[t] - S_to_E)
                    self.E_pre.append(self.Exposed[t] + S_to_E - E_to_I)
                    self.I_pre.append(self.Infected[t] + E_to_I - I_to_R)
                    self.R_pre.append(self.Resistant[t] + I_to_R)
            
            # record the estimation when we do the last iteration
            if e == (self.epoch - 1):
                    self.estimation = pd.DataFrame.from_dict({'Time':list(range(len(self.Susceptible))),
                'Estimated_Susceptible':self.S_pre, 'Estimated_Exposed': self.E_pre, 'Estimated_Infected':self.I_pre, 
                                                              'Estimated_Resistant':self.R_pre},
                orient='index').transpose()
                    self.loss = self._calculate_loss()
                    MAPE = self._calculate_MAPE()
                    MAPEtest = self._calculate_MAPE_last_5_days()
                    print("The loss in is {}".format(self.loss))
                    print("The MAPE in the whole period is {}".format(MAPE))
                    print("The MAPE in the last 5 days is {}".format(MAPEtest))
                    #print("Optimial beta is {}".format(self.rateSI))
            
            ## calculate loss in each iteration
            self.loss = self._calculate_loss()
            
            #print("The loss in iteration {} is {}".format(e, self.loss))
            #print("Current beta is {}".format(self.rateSI))  
            
            ## do beta optimation
            self._update()
            
        return self.estimation # the lastest estimation 
    
    def plot_fitted_beta_R0(self, real_obs: pandas.core.frame.DataFrame):
        fig, ax = plt.subplots(figsize=(15,6))
        plt.plot(self.estimation['Time'], self.betalist, color='green')
        Rlist = [x / self.rateIR for x in self.betalist] # transmissibility over time
        plt.plot(self.estimation['Time'], Rlist, color='blue')
        
        # set x tricks
        datemin = real_obs['date'].min()
        numdays = len(real_obs) 
        labels = list((datemin + datetime.timedelta(days=x)).strftime('%m-%d') for x in range(numdays))
        plt.xticks(list(range(numdays)), labels, rotation=90,fontsize = 10)
        plt.xlabel('2020 Date')
        plt.ylabel('Rate')
        plt.title('Fitted Dynamic Contact Rate and Transmissibility of COVID-19 over time', fontsize = 20)
        plt.legend(['Contact Rate', 'Transmissibility'], prop={'size': 12}, bbox_to_anchor=(0.5, 1.02), 
           ncol=2, fancybox=True, shadow=True)
        plt.show()
         
    def plot_fitted_result(self, real_obs: pandas.core.frame.DataFrame):
        fig, ax = plt.subplots(figsize=(15,6))
        plt.plot(self.estimation['Time'], self.estimation['Estimated_Infected'], color='green')
        plt.plot(self.estimation['Time'], real_obs['I'], color='y')
        plt.plot(self.estimation['Time'], self.estimation['Estimated_Exposed'], color='blue')
        plt.plot(self.estimation['Time'], real_obs['E'], color='royalblue')

        # set x tricks
        datemin = real_obs['date'].min()
        numdays = len(real_obs) 
        labels = list((datemin + datetime.timedelta(days=x)).strftime('%m-%d') for x in range(numdays))
        plt.xticks(list(range(numdays)), labels, rotation=90, fontsize = 10)
        plt.xlabel('2020 Date')
        plt.ylabel('Population')
        plt.title('Fitted value by Dynamic SEIR model', fontsize = 20)
        plt.legend(['Estimated Infected','Real Infected', 'Estimated_Exposed', 'Real Exposed'], prop={'size': 12}, bbox_to_anchor=(0.5, 1.02), 
           ncol=4, fancybox=True, shadow=True)
        plt.show()

    
class dynamic_SEIR:
    """
    'eons' (number of time points to model, default 1000)
    'Susceptible' (number of susceptible individuals at time 0, default 950)
    'Exposed' (number of individuals during incubation period)
    'Infected' (number of infected individuals at time 0, default 50)
    'Resistant' (number of resistant individuals at time 0, default 0)
    'rateSI' (base rate 'beta' from S to E, default 0.05)
    'rateIR' (base rate 'gamma' from I to R, default 0.01)
    'rateAl' (base rate of isolation 'altha', from E to I, default 0.1)
    """
    def __init__(self, eons=1000, Susceptible=950, Exposed = 100, Infected=50, Resistant=0, rateIR=0.01, rateAl = 0.1,
                 alpha = 0.3, c = 5, b = -10, past_days = 30):
        self.eons = eons # number of prediction days
        self.Susceptible = Susceptible
        self.Exposed = Exposed
        self.Infected = Infected
        self.Resistant = Resistant
        self.rateSI = None
        self.rateIR = rateIR
        self.rateAl = rateAl
        self.numIndividuals = Susceptible + Infected + Resistant + Exposed # total population
        self.alpha = alpha
        self.c = c
        self.b = b
        self.past_days = past_days # make prediction since the last observation
        self.results = None
        self.modelRun = False
        
    def _calculate_beta(self, c: float, t: int, alpha: float, b: float, past_days:int):
        """
        calculate beta based on some function
        """
        t = t + past_days
        return c*exp(-alpha*(t+b))*pow((1 + exp(-alpha*(t+b))),-2) 

    def run(self, death_rate):
        Susceptible = [self.Susceptible]
        Exposed = [self.Exposed]
        Infected = [self.Infected]
        Resistant = [self.Resistant]

        for i in range(1, self.eons): # number of prediction days
            self.rateSI = self._calculate_beta(c = self.c, t = i, b = self.b, 
                                               alpha = self.alpha, past_days = self.past_days)
            #print(self.rateSI)
            S_to_E = (self.rateSI * Susceptible[-1] * Infected[-1]) / self.numIndividuals
            E_to_I = (self.rateAl * Exposed[-1])
            I_to_R = (Infected[-1] * self.rateIR)
            
            Susceptible.append(Susceptible[-1] - S_to_E)
            Exposed.append(Exposed[-1] + S_to_E - E_to_I)
            Infected.append(Infected[-1] + E_to_I - I_to_R)
            Resistant.append(Resistant[-1] + I_to_R)
        
        # Death is death_rate* recovery group
        Death = list(map(lambda x: (x * death_rate), Resistant))
        # Heal is removed - Death
        Heal = list(map(lambda x: (x * (1-death_rate)), Resistant))
        self.results = pd.DataFrame.from_dict({'Time':list(range(len(Susceptible))),
            'Susceptible':Susceptible, 'Exposed': Exposed, 'Infected':Infected, 'Resistant':Resistant,
                                               'Death':Death, 'Heal': Heal},
            orient='index').transpose()
        self.modelRun = True
        return self.results

    def plot(self, title, ylabel, xlabel, starting_point):
        if self.modelRun == False:
            print('Error: Model has not run. Please call SIR.run()')
            return
        print("Maximum infected case: ",
              format(int(max(self.results['Infected']))))
        fig, ax = plt.subplots(figsize=(10,6))
        plt.plot(self.results['Time'], self.results['Susceptible'], color='blue')
        plt.plot(self.results['Time'], self.results['Infected'], color='red')
        plt.plot(self.results['Time'], self.results['Exposed'], color='orange')
        plt.plot(self.results['Time'], self.results['Resistant'], color='palegreen')
        plt.plot(self.results['Time'], self.results['Heal'], color='green')
        plt.plot(self.results['Time'], self.results['Death'], color='grey')
        # set x trick
        datemin = starting_point
        numdays = len(self.results) 
        labels = list((datemin + datetime.timedelta(days=x)).strftime('%m-%d') for x in range(numdays))
        plt.xticks(list(range(numdays)), labels, rotation=60)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(['Susceptible','Infected','Exposed','Removed', 'Heal', 'Death'], prop={'size': 12}, bbox_to_anchor=(0.5, 1.02), ncol=6, fancybox=True, shadow=True)
        plt.title(title, fontsize = 20)
        plt.show()
        
    def plot_noSuscep(self, title, ylabel, xlabel, starting_point):
        if self.modelRun == False:
            print('Error: Model has not run. Please call SIR.run()')
            return
        print("Maximum infected case: ",
              format(int(max(self.results['Infected']))))
        fig, ax = plt.subplots(figsize=(10,6))
        plt.plot(self.results['Time'], self.results['Infected'], color='red')
        plt.plot(self.results['Time'], self.results['Resistant'], color='palegreen')
        plt.plot(self.results['Time'], self.results['Exposed'], color='orange')
        plt.plot(self.results['Time'], self.results['Heal'], color='green')
        plt.plot(self.results['Time'], self.results['Death'], color='grey')
        # set x trick
        datemin = starting_point
        numdays = len(self.results) 
        labels = list((datemin + datetime.timedelta(days=x)).strftime('%m-%d') for x in range(numdays))
        plt.xticks(list(range(numdays)), labels, rotation=60)
        
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(['Infected','Removed','Exposed','Heal','Death'], prop={'size': 12}, bbox_to_anchor=(0.5, 1.02), ncol=5, fancybox=True, shadow=True)
        plt.title(title, fontsize = 20)
        plt.show()    
    
    
    