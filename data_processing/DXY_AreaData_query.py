# Query real time data from DingXiangYuan, and keep the latest records every day for each city

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 12:41:50 2020

@author: leebond

resource: https://github.com/jianxu305/nCov2019_analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import pickle as pkl
import numpy as np
import pandas
import datetime
import math
import os
import warnings
warnings.filterwarnings('ignore')
from googletrans import Translator # package used to translate Chinese into English


translator = Translator()
## Resoruce for Chinese - English Translation
## Resoruce for Chinese - English Translation
with open('chineseProvince_to_EN.pkl','rb') as f:
    prov_dict = pkl.load(f)
with open('chineseCity_to_EN.pkl','rb') as f:
    city_dict = pkl.load(f)    
    

def isNaN(num):
    return num != num

def add_days(DXYArea: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """
    Create a new column: Days, number of days after 2019-12-08 (detect the first case)
    """
    DXYArea['date'] = pd.to_datetime(DXYArea['date'])
    first_day = datetime.datetime(2019, 12, 8) # the time when detected the first case (2019-12-08)
    DXYArea['Days'] = (DXYArea['date'] - first_day).dt.days
    return DXYArea

def add_net_confirmed_case(DXYArea: pd.core.frame.DataFrame)-> pd.core.frame.DataFrame:
    """
    Add net confirmed case = confirmed - cured - dead
    """
    DXYArea['net_confirmed'] = DXYArea['confirmed'] - DXYArea['cured'] - DXYArea['dead']
    return DXYArea


        
def isNaN(num):
    return num != num

## Resoruce for Chinese - English Translation
with open('chineseProvince_to_EN.pkl','rb') as f:
    prov_dict = pkl.load(f)

    
with open('chineseCity_to_EN.pkl','rb') as f:
    city_dict = pkl.load(f)    
        
def translate_to_English(data, prov_dict, city_dict):
    """Translate Chinese in dataset to English
    """        
    data['province'] = data['province'].apply(getProvinceTranslation)
    data['city'] = data['city'].apply(getCityTranslation)
    
    for city in unable_translation: # remove these unable translated data
        data = data[data['city']!=city]
    return data
    
def getProvinceTranslation(name):
    if not isNaN(name):
        return prov_dict[name]
    else: 
        return name

unable_translation = []
def getCityTranslation(name):
    try:
        if not isNaN(name): 
            return city_dict[name]
        else:
            return name
    except:
        unable_translation.append(name)
        #print(name + ' cannot be translated\n')
        return name
        
def main():
    
    ## Query the latest data
    os.system('python dataset.py')
    
    DXYArea = pd.read_csv('../data/DXY_Chinese.csv') # Read Chinese version 
    # select column
    DXYArea = DXYArea[['date','country','countryCode','province', 'city', 'confirmed', 'suspected', 'cured', 'dead']]

    
    daily_frm_DXYArea = translate_to_English(DXYArea, prov_dict, city_dict)
    
    daily_frm_DXYArea = add_days(daily_frm_DXYArea)  # add the number of days after 2019-12-08
    daily_frm_DXYArea = add_net_confirmed_case(daily_frm_DXYArea) # add net confirmed case
    
    daily_frm_DXYArea.to_csv('../data/DXYArea.csv', index = None, header=True)
    
    print("Save area daily dataset (English) into ../data/DXYArea.csv")
    
if __name__ == '__main__':
    main()