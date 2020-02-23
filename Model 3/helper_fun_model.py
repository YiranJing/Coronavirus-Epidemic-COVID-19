### Helper function for simulation model

#### Author: Yiran Jing
#### Date: Feb 2020

import pandas as pd
import numpy as np
import operator
import matplotlib.pyplot as plt
import pandas as pd
import pandas
import datetime
import matplotlib.dates as mdates
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import Ridge, RidgeCV, ElasticNet, LassoCV, LassoLarsCV, LinearRegression, ElasticNetCV
from sklearn.preprocessing import PolynomialFeatures
import warnings
warnings.filterwarnings('ignore')

########################
## dataset help function
########################

def get_province_df(df, provinceName: str) -> pandas.core.frame.DataFrame:
    """
    Return time series data of given province
    """
    return df[(df['province']==provinceName) & (df['city'].isnull())]


def get_China_total(df) -> pandas.core.frame.DataFrame:
    """
    Return time series data of China total (including HK and Taiwan)
    """
    return df[(df['countryCode']=='CN') & (df['province'].isnull())]

def get_China_exclude_province(df, provinceName: str)-> pandas.core.frame.DataFrame:
    """
    Return time series data of China total exclude the given province
    """
    Hubei= get_province_df(df, provinceName)
    China_total = get_China_total(df)
    
    NotHubei = China_total.reset_index(drop= True)
    Hubei = Hubei.reset_index(drop= True)
    
    NotHubei['E'] = NotHubei['E'] - Hubei['E']
    NotHubei['R'] = NotHubei['R'] - Hubei['R']
    NotHubei['I'] = NotHubei['I'] - Hubei['I']
    
    return NotHubei



##################
## Clean data
##################

def split_train_test_by_date(df: pandas.core.frame.DataFrame, ndays = 3):  ## parameterized split range
    """
    Separate Train and Test dataset in time series
    """
    # we use the last 3 days as test data
    split_date = df['date'].max() - datetime.timedelta(days=ndays)
    
    ## Separate Train and Test dataset
    Train = df[df['date'] < split_date]
    Test = df[df['date'] >= split_date]
    print("Train dataset: data before {} \nTest dataset: the last {} days".format(split_date, ndays))
    
    return Train, Test

def data_processing(df, ndays = 3):

    overall_df = pd.DataFrame(df.groupby(['date']).agg({'confirmed': "sum",
                                                                'cured': "sum",
                                                                'dead': 'sum',
                                                                'Days': 'mean'})).reset_index()
    Train, Test = split_train_test_by_date(overall_df, ndays)

    X_train = Train['Days']
    y_train = Train['confirmed']
    X_test =  Test['Days']
    y_test = Test['confirmed']
    return X_train, X_test, y_train, y_test

##################
###           EDA
##################

def tsplot_conf_dead_cured(df, title_prefix, figsize=(13,10), fontsize=18, logy=False):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    plot_df = df.groupby('date').agg('sum')
    plot_df.plot(y=['confirmed'], style='-*', ax=ax1, grid=True, figsize=figsize, logy=logy, color='black', marker='o')
    if logy:
        ax1.set_ylabel("log(confirmed)", color="black", fontsize=14)
    else:
        ax1.set_ylabel("confirmed", color="black", fontsize=14)
    if 'dailyNew_confirmed' in df.columns:
        ax11 = ax1.twinx()
        ax11.bar(x=plot_df.index, height=plot_df['dailyNew_confirmed'], alpha=0.3, color='blue')
        ax11.set_ylabel('dailyNew_confirmed', color='blue', fontsize=14)
    ax2 = fig.add_subplot(212)
    plot_df.plot(y=['dead', 'cured'], style=':*', grid=True, ax=ax2, figsize=figsize, sharex=False, logy=logy)
    ax2.set_ylabel("count")
    title = title_prefix + ' Cumulative Confirmed, Death, Cure'
    fig.suptitle(title, fontsize=fontsize)
    
def draw_province_trend(title_prefix: str, df: pandas.core.frame.DataFrame):
    """
    df is the daily dataset from DXY
    """
    sub_df = df[df['province'] == title_prefix]
    tsplot_conf_dead_cured(sub_df, title_prefix)
    
def draw_city_trend(title_prefix: str, df: pandas.core.frame.DataFrame):
    """
    df is the daily dataset from DXY
    """
    sub_df = df[df['city'] == title_prefix]
    tsplot_conf_dead_cured(sub_df, title_prefix)

##################
###      feature engineering
##################

def feature_engineering(df:pandas.core.frame.DataFrame, features_to_engineer):
    for feature in features_to_engineer:
        df[f'{feature}_lag1'] = df[f'{feature}'].shift()
        df[f'{feature}_lag1'].fillna(0, inplace = True)
    return df
    

###################
##  Modelling
###################

### polynomial_regression
def as_arrary(x):
    return [np.asarray(x)]

def draw_fit_plot(degree: int, area: str, X_train, X_test, y_train, y_test, y_train_predicted, y_test_predict, df):
    if len(y_test)>0:
        x = pd.Series(np.concatenate((X_train, X_test)))
        y = pd.Series(np.concatenate((y_train, y_test)))
    else:
        x = X_train; y = y_train
    
    fig, ax = plt.subplots()
    #fig.canvas.draw()
    plt.scatter(x, y, s=10, c = 'black')
    plt.plot(X_train, y_train_predicted, color='green')
    plt.plot(X_test, y_test_predict, color = 'blue')
    plt.title("Polynomial Regression {} with degree = {}".format(area, degree))
    plt.ylabel('Confirmed cases')
    plt.xlabel('2020 Date')
    
    datemin = df['date'].min()
    numdays = len(X_train) + len(X_test)
    labels = list((datemin + datetime.timedelta(days=x)).strftime('%m-%d') for x in range(numdays))
    
    x = pd.Series(np.concatenate((X_train, X_test)))
    plt.xticks(x, labels,rotation=60)
    #fig.autofmt_xdate() # axes up to make room for them
    
    plt.show()
    

def create_polynomial_regression_model(degree:int, area:str, df,
                                       X_train: pandas.core.frame.DataFrame, 
                                       X_test: pandas.core.frame.DataFrame,
                                       y_train: pandas.core.frame.DataFrame, 
                                       y_test: pandas.core.frame.DataFrame,
                                       draw_plot = False):
    "Creates a polynomial regression model for the given degree"
    
    poly_features = PolynomialFeatures(degree=degree)
      
    # transforms the existing features to higher degree features.
    X_train_array = tuple(map(as_arrary, list(X_train)))
    X_test_array = tuple(map(as_arrary, list(X_test)))
    
    # Normalize input data
    X_train_poly = poly_features.fit_transform(X_train_array)
    
    # fit the transformed features to Linear Regression
    poly_model = LinearRegression()
    poly_model.fit(X_train_poly, y_train)
      
    # predicting on training data-set
    y_train_predicted = poly_model.predict(X_train_poly)
      
    # predicting on test data-set
    y_test_predict = poly_model.predict(poly_features.fit_transform(X_test_array))
      
    # evaluating the model on training dataset
    rmse_train = np.sqrt(mean_squared_error(y_train, y_train_predicted))
    r2_train = r2_score(y_train, y_train_predicted)
    mape_train = np.mean(np.abs((y_train-y_train_predicted))/np.abs(y_train)) 
    print("Degree {}:".format(degree))
    print("RMSE of training set is {}".format(rmse_train))
    print("R2 score of training set is {}".format(r2_train))
    print("MAPE of training set is {}\n".format(mape_train))
    
    if len(y_test)>0:
        # evaluating the model on test dataset
        rmse_test = np.sqrt(mean_squared_error(y_test, y_test_predict))
        r2_test = r2_score(y_test, y_test_predict)
        mape_test = np.mean(np.abs((y_test-y_test_predict))/np.abs(y_test))
        print("RMSE of test set is {}".format(rmse_test))
        print("R2 score of test set is {}".format(r2_test))
        print("MAPE of test set is {}".format(mape_test))
        
    print('---------------------------------------\n')
    
    # Draw fit plot
    if draw_plot == True: 
        draw_fit_plot(degree, area, X_train, X_test, y_train, y_test, y_train_predicted, y_test_predict, df)


def forecast_next_4_days(degree: int, area:str, df: pandas.core.frame.DataFrame):
    """
    Use all observations to train, based on the 
    """
    X_train = df['Days']
    y_train = df['confirmed']
    
    # Create dataset for next 4 days
    X_test = [df['Days'].max() + 1, df['Days'].max() + 2, df['Days'].max() + 3, df['Days'].max() + 4]
    y_test = []
    
    create_polynomial_regression_model(degree, area, df, X_train, X_test, y_train, y_test, draw_plot = True)
    
    
#############################
###  model selection
#############################


def rmse_cv_train(model):
    rmse= np.sqrt(-cross_val_score(model, X_train, y_train, scoring="neg_mean_squared_error", cv = 5))
    return(rmse)

def rmse_cv_test(model):
    rmse= np.sqrt(-cross_val_score(model, X_test, y_test, scoring="neg_mean_squared_error", cv = 5))
    return(rmse)

def mae_cv_train(model):
    mae= -cross_val_score(model, X_train, y_train, scoring="neg_mean_absolute_error", cv = 5)
    return(mae)

def mae_cv_test(model):
    mae= -cross_val_score(model, X_test, y_test, scoring="neg_mean_absolute_error", cv = 5)
    return(mae)

def mape_no_cv(model, X, y):
    y_pred = model.predict(X)
    mape = np.abs((y-y_pred))/np.abs(y) # Check this definition
    return np.mean(mape)
    
def mae_no_cv(model, X, y):
    y_pred = model.predict(X)
    return mean_absolute_error(y, y_pred) # Check the order of the inputs here

def r2_no_cv(model, X, y):
    y_pred = model.predict(X)
    return r2_score(y, y_pred)

def get_validation_score(model, X, y):
    print("Linear Regression MAPE on Validation set :", mape_no_cv(model, X, y))
    print("Linear Regression MAE on Validation set :", mae_no_cv(model, X, y))
    print("Linear Regression R2 on Validation set :", r2_no_cv(model, X, y))
    

    