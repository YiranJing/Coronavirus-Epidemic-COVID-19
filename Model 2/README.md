
# Model 2: Simulating Peak of 2019-nCoV in Wuhan after 23 Jan

***

## Usage:
- Choice 1: Run [Forecast_Outbreak_Wuhan.ipynb](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202/Forecast_Outbreak_Wuhan.ipynb)

- Choice 2:
```sh
pip install -r ../requirements.txt
python run_model2.py
```
### Detail
   > Method: SIER (susceptible-exposed-infectious- recovered) model and Sensitivity analysis

   > Reference: [Nowcasting and forecasting the potential domestic and international spread of the 2019-nCoV outbreak (Jan 31)](https://www.thelancet.com/action/showPdf?pii=S0140-6736%2820%2930260-9)

   - **Main Conclusion:** (using Chinese official data between 2019-12-08 and 2020-02-02)
      - **Estimated initial transmissibility R0 (the basic reproduction number) of 2019-nCoV: 2.9**
      - **Estimated Maximum infected case in Wuhan: more than 14000 (peak, not cumulative)**
      - **Consider inadequate medical resources and under-reported official data, Maximum infected case (peak, not cumulative) in Wuhan might between 16000 and 25000**
      - **Based on official news on 02 Feb, human control is still limited to control the transmissibility. in this situation, Maximum infected case (peak, not cumulative) in Wuhan can more than 100 thousand or even 150 thousand**
      - **The peak will appear after 22 Feb, 2020**
      - Close City policy has significant control for 2019-nCoV, otherwise, the infected cases may up to 200 thousand.
   - Key assumptions within this Model:
      - Exposed group (individuals during incubation period) is 4 times larger than Infective group (4109 confirmed cases until 02 Feb)
      - After 23 Jan, confirmed cases will be isolated.
      - Assume the death rate is 3% (official number).
      - Before 23 Jan, 1 case can infect 5 people on average. While after 23 Jan, only 1 people a case may infect.
      - Before 23 Jan, the population in Wuhan is 11 million. After 23 Jan, population in Wuhan is 9 million.
      - The mean of incubation period is 7 days, and the mean duration of the infection is 14 days.
      - Wuhan has adequate medical resources and the official number is correct.
![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202/image/withControl.png)

Note:
- Removed: heal or death
- Death: Removed group * death_rate
- Exposed: individuals during incubation period
- Susceptible: Healthy people
- Infected: Confirmed cases
![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202/image/iamges-SIER.png)

### Sensitivity Analysis
#### Case 1: Official under-report Data: Sensitivity Analysis using the conclusion of [Model 1](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)
   - Wuhan has 38500 cases until 23 Jan, and 80% of them are in incubation period.
   - Assume the death rate = cure rate = 3% (official number)
   - **Estimated Maximum infected case in Wuhan: more than 22000**
#### Case 2: Sensitivity Analysis under inadequate medical resources
   - Suppose the mean duration of the infection is 20 days, rather than 14 days.
   - Estimated initial transmissibility R0 (the basic reproduction number) of 2019-nCoV: 3.7
   - **Estimated Maximum infected case in Wuhan: more than 16000** under official data

#### Case 3: Sensitivity Analysis considering higher transmission probability
   > Dr.Lanjuan Li on feb 02 said that due to limited testing kits and imperfect isolation, some cases cannot be detected correctly or immediately, Also not perfect isolation
   > 2019-nCoV has lots of transmission ways, thus harder to prevent than other epidemic.

   - Suppose after 23 Jan, 2 people a case may infect
   - **Estimated Maximum infected case in Wuhan: more than 100000** under official data

#### Case 4: Official under-report Data + inadequate medical resources
   - Suppose the mean duration of the infection is 20 days
   - Suppose Wuhan 38500 cases until 23 Jan, and 80% of them are in incubation period
   - **Estimated Maximum infected case in Wuhan: more than 25000**

#### Case 5: Official under-report Data + inadequate medical resources + higher transmission probability
      - Suppose the mean duration of the infection is 20 days
      - Suppose Wuhan 38500 cases until 23 Jan, and 80% of them are in incubation period
      - Suppose after 23 Jan, 2 people a case may infect
      - **Estimated Maximum infected case in Wuhan: more than 150000**
