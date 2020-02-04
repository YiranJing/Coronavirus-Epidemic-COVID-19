# Nowcasting and Forecasting the 2019-nCoV Outbreak size in Wuhan

[简体中文](README.md) | English

#### Date: Since Jan 26 2020

***

## Projects:
> On January 23, authorities in Wuhan shut down the city’s public transportation, including buses, trains, ferries, and the airport.
> There are 9 million people stay in Wuhan after 23 Jan. And official reported that 5 million people travel out Wuhan for Chinese Spring Festival. The effective catchment population of Wuhan international airport is around 19 million.

Consider the transmissibility and population of Wuhan changed a lot before and after Jan 23, 2020, I choice different methods to nowcasting and forecasting the potential outbreak size in Wuhan referencing by published papers.
### Model 1: [Estimating the potential number of cases in Wuhan until Jan 23](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)😷
   - Author: Yiran Jing
   - **Main Conclusion: There are more than 38500 cases 95% CI(30000, 48470) until Jan 23**, based on 29 Jan data.
   > Method: Considering Wuhan is the major air and train transportation hub of China, we use the number of cases exported from Wuhan internationally as the sample, assuming the infected people follow a Possion distribution, then calculate the 95% confidence interval by profile likelihood method. Sensitivity analysis followed by.

   > Reference: [report2 (Jan 21)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf)

### Model 2: [Simulating Peak of 2019-nCoV in Wuhan after 23 Jan](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202)📈
   - Author: Yiran Jing
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














***
***
## Other Insightful 2019-nCoV projects on github
### Visualization
1. Time series Visualisation Dashboard (Jan 21- Feb 1)
![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/ncov.gif)
   - Author: [P. Daniel Tyreus](https://github.com/pdtyreus)
   - [original repo](https://github.com/pdtyreus/coronavirus-ds)
   - [Time series visualisation by geopandas](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Visualization)
2. [Real time visualisation by province, China](https://yiqing.ahusmart.com/)
   - Author: [Kai Fang](https://github.com/hack-fang)
   - [original repo](https://github.com/hack-fang/nCov)

### Real-Time Data Sources
1. [Modelling of the nCoV-2019 outbreak in Wuhan](https://github.com/chrism0dwk/wuhan)
    - Author: Jon Read, Jess Bridgen, and Chris Jewell at Lancaster University
1. [微信公众号实时查询感染人数](https://github.com/echo-cool/2019-nCov)
    - Author: [echo-cool](https://github.com/echo-cool)
2. [2019新型冠状病毒疫情实时爬虫](https://github.com/BlankerL/DXY-2019-nCoV-Crawler)
    - Author: [Isaac Lin](https://github.com/BlankerL)
1. [新增肺炎微博超话爬取数据](https://github.com/czy1999/weibo-topic-spider)
    - Author: [czy1999](https://github.com/czy1999)


***

### Key Reference
1. [Early Transmission Dynamics in Wuhan (Jan 29)](https://www.nejm.org/doi/full/10.1056/NEJMoa2001316)
1. [Nowcasting and forecasting the potential domestic and international spread of the 2019-nCoV outbreak using Markov Chain Monte Carlo methods](https://www.thelancet.com/action/showPdf?pii=S0140-6736%2820%2930260-9)
2. [Estimating the potential total number of novel
Coronavirus cases in Wuhan City, China (Jan 21 2020)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf)
    - [Statistical model and Python code](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)
3. [Transmissibility of 2019-nCoV (Jan 24)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-2019-nCoV-transmissibility.pdf)
4. [Epidemic Prediction by UK scientists (Jan 24 2020)](https://www.medrxiv.org/node/71375.external-links.html)


***
## Welcome to join us!!
Please connect with me if you are interested in this project!

- Email: yjin5856@uni.sydney.edu.au
- Wechat: A570281374
