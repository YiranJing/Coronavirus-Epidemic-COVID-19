# Nowcasting and Forecasting the 2019-nCoV Outbreak

[简体中文](README.md) | English

#### Date: Since Jan 26 2020

## Contents：
1. Nowcasting and Forecasting the 2019-nCoV Outbreak size in Wuhan
   > MSE, basic SEIR model, sentiment analysis
   > [Overview of SEIR model](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/SEIR_model3.pdf)
   - Model 1: Estimating the potential number of cases in Wuhan until Jan 23
   - Model 2: Simulating Peak of 2019-nCoV in Wuhan after 23 Jan

2. Model 3: Real-Time forecasting of the confirmed cases in China in the next 2 months
   > Baseline: Ridge regression, improved by Dynamic SEIR model <br />
   > Author: [Shih Heng Lo](https://github.com/Harrisonust); Yiran Jing

   - Prediction for China total trend
   - Prediction for Hubei and ex-hubei trend

#### Key limitation within models below:
1. My models conclusions are critically dependent on the assumptions underpinning models.
   - Adjustments are considered by sensitivity analysis (but not enough)
2. The model s' structures are quite simple, haven't combine enough information, so cannot get really good or robust result.
   - But for the prediction of Wuhan City only, maybe enough.
   - Will keep updating model based on the latest information.

#### Main Challenges for all predictions:
1. We have limited understanding of this new disease
   - For example, we did not test all  people with 2019-nCoV correctly. (unclear symptoms: whether people with 2019-nCoV who do not have symptoms can transmit an infection)
2. It is hard to get the real-time correct information. (official Chinese data is under-report 100% ), especially for Wuhan.
   - For example, we do not know how many people infected when wuhan shut down.
3. The prediction is highly sensitive to the policy
   - (for example, travel restriction,  force people stay in home, wuhan build 3 new hospital for 2019-nCoV etc. ), all of these policies influenced a lot on the time-line. **When we do prediction, our key assumption is no new policy in the future**.

#### Data
[Real-time data query and save to csv](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/data_processing)

***

### Nowcasting and Forecasting the 2019-nCoV Outbreak size in Wuhan (Model 1 and 2)
> On January 23, authorities in Wuhan shut down the city’s public transportation, including buses, trains, ferries, and the airport.
> There are 9 million people stay in Wuhan after 23 Jan. And official reported that 5 million people travel out Wuhan for Chinese Spring Festival. The effective catchment population of Wuhan international airport is around 19 million.

Consider the transmissibility and population of Wuhan changed a lot before and after Jan 23, 2020, I choice different methods to nowcasting and forecasting the potential outbreak size in Wuhan city referencing by published papers.

### Model 1: [Estimating the potential number of cases in Wuhan until Jan 23](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)😷
   - Author: Yiran Jing
   - **Main Conclusion (_within Wuhan City only_): There are more than 38500 cases 95% CI(30000, 48470) until Jan 23**, based on 29 Jan data.
   > Method: Considering Wuhan is the major air and train transportation hub of China, we use the number of cases exported from Wuhan internationally as the sample, assuming the infected people follow a Possion distribution, then calculate the 95% confidence interval by profile likelihood method. Sensitivity analysis followed by.

   > Reference: [report2 (Jan 21)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf)

### Model 2: [Simulating Peak of 2019-nCoV in Wuhan after 23 Jan](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202)📈
   - Author: Yiran Jing
   > Method: Deterministic SEIR (susceptible-exposed-infectious- recovered) model and Sensitivity analysis

   > Reference: [Nowcasting and forecasting the potential domestic and international spread of the 2019-nCoV outbreak (Jan 31)](https://www.thelancet.com/action/showPdf?pii=S0140-6736%2820%2930260-9)

   - **Main Conclusion (_within Wuhan City only_):** (using Chinese official data between 2019-12-08 and 2020-02-02)
      - Estimated initial transmissibility **R0** (the basic reproduction number) of 2019-nCoV: **2.9**
      - **Under the most optimistic estimate, the maximum infected case in Wuhan: more than 14000 (peak, not cumulative)** (_the peak of red line of the plot below._) **And the cumulative number of cases in the whole period is around 50 thousand** (_the green line_).
      - **Truth 1**: Consider inadequate medical resources and under-reported official data, Maximum infected case (peak, not cumulative) in Wuhan might between 16000 and 25000
      - **Truth 2**: Risk of transmission is still high between 23 Jan and 04 Feb, and begin to decrease after 5 Feb.
         > Based on official news on 2 Feb, cases cannot be detected immediately, also not perfect isolation. Under this situation, Maximum infected case (peak, not cumulative) in Wuhan can more than 100 thousand or even 150 thousand. (suppose k=2)

         > Update: 3 new hospitals begin to accept patents after 5 Feb.(can accept around 6 thousand patients total). Now the risk of transmission is decrease, since more patients can be in hospitals and isolated.


      - **Consider truth 1 and 2, the maximum infected case (peak, not cumulative) in Wuhan maybe between 25 thousand and 100 thousand**.
      - **The peak will appear after 22 Feb, 2020**
      - Close City policy has significant control for 2019-nCoV, otherwise, the peak of infected cases may up to 200 thousand.
***

## Model 3:[Real-Time forecasting of the confirmed cases in China in the next 2 months](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%203)📉
   - Author: [Shih Heng Lo](https://github.com/Harrisonust); Yiran Jing
   > Method: Dynamic SEIR (susceptible-exposed-infectious- recovered) model, Gradient Descent
   > Model comparison based on the test score (MAPE) of last 5 days, baseline is [ridge Ridge regression](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%203/Baseline_RidgeRegression.ipynb)
   > Reference: [Dynamic SIR model](https://github.com/Harrisonust/Machine-Learning/tree/master/nCoV2)

   - **Main Conclusion (China TOtal):** (using Chinese official data between 2019-12-08 and 2020-02-13)
      - **The number of net confirmed cases will exceed 60000, and the peak can be reach before 20 Feb**.
      - **The transmissibility has been controlled from initial 3.2(R0) to less than 0.5**.
      - **The estimated number of infected case will be less than 4000 in early April**
  - Model assumptions: [Overview of SEIR model](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/SEIR_model3.pdf)
      - Constant (closed) population size:  Due to the international travel ban, strict home quarantine rules in China and the low death rate of COVID-19 (less than 2%), we can assume the China population is constant.
      - In SEIR models, the exposed individuals is infected but not yet infectious, and the first transmission can only happen after symptoms appear. However, InCOVID-19 case, we know that individuals are infectious during the whole incubation period. Assume latent period is the same as incubation.
      - Suppose the average duration of recovery is 14 days, which is similar with SARS
      - Suppose the total number of individuals within incubation period is 4 time of susceptible case reported by CCDI.
      - Assume the died people is around 2%, belonging to removed individuals (R).


![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/image/dynamic_SEIR.png)

The red line shows the trend of net confirmed cases in the next 50 days.
Note:
- Removed: heal or death
- Death: Removed group * death_rate
- Exposed: individuals during incubation period
- Susceptible: Healthy people
- Infected: Confirmed cases

#### Model performance
The mean absolute percentage error (MAPE) is a measure of prediction accuracy of a forecasting method in statistics. The MAPE of confirmed cases using data between 2020- 2-14 to 2020-02-22 is 0.0066. The figure below visualizes the real observation and the SEIR model predictions for the next 9 days. Overall, SEIR model predicts well for the peaking time and the general trend.

![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/image/SEIR_test_7days.png)


#### Dynamic contact rate β as a function of time t
Optimization algorithm Gradient Descent
![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/image/beta.png)





***
## Real-Time forecasting of the confirmed cases in China

Estimating the confirmed cases of China in the next few days based on the latest data from DingXiangYuan

#### Real-time data query Step:
1. Query the latest data from DingXiangYuan
```sh
## Update data from DXY
$ cd data_processing && python DXY_AreaData_query.py # save data out to data folder.
```

***
## Visualization

##### The best visualization of 2019-nCoV in China
![image](https://github.com/Mistletoer/NCP-historical-data-visualization/blob/master/demo.gif)
- Author: [Minghou Lei](https://github.com/Mistletoer)
- [Origin Github](https://github.com/Mistletoer/NCP-historical-data-visualization-2019-nCoV-)

##### Dashboard overseas
[CoronaTracker Analytics Dashboard](https://www.coronatracker.com/analytics/)

My current study and tasks are updated here: [Project](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/projects/1)

Welcome to connect with me if you are interested in this project!

- Email: yjin5856@uni.sydney.edu.au
- Wechat: A570281374
