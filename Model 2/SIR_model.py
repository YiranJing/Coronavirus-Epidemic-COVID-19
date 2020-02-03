## SIR model
## Author: Yran Jing
## Date: 2020-02-02
## Moddified based on https://github.com/mattravenhall/BasicSIRModel

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

class SIR:
    """
    'eons' (number of time points to model, default 1000)
    'Susceptible' (number of susceptible individuals at time 0, default 950)
    'Infected' (number of infected individuals at time 0, default 50)
    'Resistant' (number of resistant individuals at time 0, default 0)
    'rateSI' (base rate 'beta' from S to I, default 0.05)
    'rateIR' (base rate 'gamma' from I to R, default 0.01)
    """
    def __init__(self, eons=1000, Susceptible=950, Infected=50, Resistant=0, rateSI=0.05, rateIR=0.01):
        self.eons = eons
        self.Susceptible = Susceptible
        self.Infected = Infected
        self.Resistant = Resistant
        self.rateSI = rateSI
        self.rateIR = rateIR
        self.numIndividuals = Susceptible + Infected + Resistant
        self.results = None
        self.modelRun = False

    def run(self):
        Susceptible = [self.Susceptible]
        Infected = [self.Infected]
        Resistant = [self.Resistant]

        for step in range(1, self.eons):
            S_to_I = (self.rateSI * Susceptible[-1] * Infected[-1]) / self.numIndividuals
            I_to_R = Infected[-1] * self.rateIR
            Susceptible.append(Susceptible[-1] - S_to_I)
            Infected.append(Infected[-1] + S_to_I - I_to_R)
            Resistant.append(Resistant[-1] + I_to_R)

        self.results = pd.DataFrame.from_dict({'Time':list(range(len(Susceptible))),
            'Susceptible':Susceptible, 'Infected':Infected, 'Resistant':Resistant},
            orient='index').transpose()
        self.modelRun = True
        return self.results

    def plot(self, title, ylabel):
        if self.modelRun == False:
            print('Error: Model has not run. Please call SIR.run()')
            return
        print("Maximum infected case: ",
              format(int(max(self.results['Infected']))))
        fig, ax = plt.subplots(figsize=(10,6))
        plt.plot(self.results['Time'], self.results['Susceptible'], color='blue')
        plt.plot(self.results['Time'], self.results['Infected'], color='red')
        plt.plot(self.results['Time'], self.results['Resistant'], color='green')
        plt.xlabel('Days')
        plt.ylabel(ylabel)
        plt.legend(['Susceptible','Infected','Removed'], prop={'size': 10}, bbox_to_anchor=(0.5, 1.02), ncol=3, fancybox=True, shadow=True)
        plt.title(title, fontsize = 20)
        plt.show()
        
    def plot_noSuscep(self, title, ylabel):
        if self.modelRun == False:
            print('Error: Model has not run. Please call SIR.run()')
            return
        print("Maximum infected case: ",
              format(int(max(self.results['Infected']))))
        fig, ax = plt.subplots(figsize=(10,6))
        plt.plot(self.results['Time'], self.results['Infected'], color='red')
        plt.plot(self.results['Time'], self.results['Resistant'], color='green')
        plt.xlabel('Days')
        plt.ylabel(ylabel)
        plt.legend(['Infected','Removed'], prop={'size': 10}, bbox_to_anchor=(0.5, 1.02), ncol=2, fancybox=True, shadow=True)
        plt.title(title, fontsize = 20)
        plt.show()
        