# 估计和预测 2019-nCoV 新型冠状病毒在武汉的爆发情况

简体中文 | [English](README.en.md)

#### 日期: 2020年1月

***

## 项目:
> 2020年1月23日，交通枢纽的武汉市被封城。900万人民被困在武汉市区。在此之前，有500万人因春节离开武汉。估计机场的国际人流量为1900万。

考虑到新型武汉肺炎的快速传播性和武汉居住人口在封城前后变化巨大，我选择了不同的模型来估计封城前后武汉的感染人数，主要参考和借鉴今日发表的相关论文，数据参考官方数据。

### 模型 1: [估计武汉封城时的感染人数](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)
   - 作者: 景怡然
   - **主要结论： 截止1月23日，武汉有超过 38500 名感染者加确诊者，95%置信区间(30000, 48470)**，根据1月29号海外发现的感染人数计算，引用2018年的交通数据估算。
   > Method: Considering Wuhan is the major air and train transportation hub of China, we use the number of cases exported from Wuhan internationally as the sample, assuming the infected people follow a Possion distribution, then calculate the 95% confidence interval by profile likelihood method. Sensitivity analysis followed by.
   
   > Reference: [report2 (Jan 21)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf)

### 模型 2: [模拟预测封城以后武汉肺炎的感染人数以及峰值](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202/Forecast_Outbreak_Wuhan.ipynb)
   - 作者: 景怡然
   > Method: SIER (susceptible-exposed-infectious- recovered) model and Sensitivity analysis
   
   > Reference: [Nowcasting and forecasting the potential domestic and international spread of the 2019-nCoV outbreak (Jan 31)](https://www.thelancet.com/action/showPdf?pii=S0140-6736%2820%2930260-9)

   - **主要结论:** (根据 2019-12-08 至 2020-02-02 的官方数据)
      - **估计最初的传播速率 R0 (基本传染数) 为: 2.9**
      - **估计武汉肺炎的患者会超过1万人，峰值最早在2月中旬出现**
      - 封城措施对控制病情有非常显著的作用: 根据模型估算，如果不封城，仅仅隔离患者，武汉患者峰值可能会高达20万。
   - 模型主要假设:
      - 潜伏人群是确诊病例的五倍。(确诊病例按照4109计算，截止2月2日)
      - 23号封城以后，所有确诊病例都会被严格隔离
      - 23号之前，平均一个感染者会传染5个人；23号以后，平均一个感染者最多只会传染1个人
      - 23号之前，武汉人口为1100万；23号后，武汉人口为900万
      - 平均潜伏期为7天，恢复期约为14天。
![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202/image/withControl.png)
注释:
- Removed(移除人群): 治愈或者死亡
- Exposed(潜伏人群): 在潜伏期的患者
- Susceptible(易感人群): 健康但有风险被感染的人群
- Infected(确诊并隔离患者): 确诊人群
![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202/image/SIER2.png)
#### 用[模型 1]的结论做敏感度分析测试(https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)
  - 在1月23号有38500名感染者，假设其中80%在潜伏期，其余为有明显症状患者
  - 假设目前死亡率等于治愈率，均为3% （根据官方数字）
  - **估计武汉患者最多可超过2.2万人**



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


***
## Data Sources
- Merged Dataset output: [data/mergedData/combined.csv](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/data/mergedData/combined.csv)
- Referenced: [coronavirus-ds](https://github.com/pdtyreus/coronavirus-ds)
The data for tracking the 2019-nCoV outbreak is provided by the [Johns Hopkins Center for Systems Science and Engineering](https://systems.jhu.edu/research/public-health/ncov/)

#### Pulling Updates from Google Sheets

The data is updated in a read-only [Google Sheet](https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w).

Download credentials and install dependencies as described [in the Google documentation.](https://developers.google.com/sheets/api/quickstart/python).

```shell script
python pull_gsheet_csse.py  # within data folder
```


***

### Key Reference
1. [Early Transmission Dynamics in Wuhan (Jan 29)](https://www.nejm.org/doi/full/10.1056/NEJMoa2001316)
1. [Nowcasting and forecasting the potential domestic and
international spread of the 2019-nCoV outbreak using Markov Chain Monte Carlo methods](https://www.thelancet.com/action/showPdf?pii=S0140-6736%2820%2930260-9)
2. [Estimating the potential total number of novel
Coronavirus cases in Wuhan City, China (Jan 21 2020)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf)
    - [Statistical model and Python code](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)
3. [Transmissibility of 2019-nCoV (Jan 24)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/Imperial-2019-nCoV-transmissibility.pdf)
4. [Epidemic Prediction by UK scientists (Jan 24 2020)](https://www.medrxiv.org/node/71375.external-links.html)


***
## 欢迎加入!!
请联系我如果你对肺炎相关项目感兴趣，不管是统计模型还是数据可视化等等！

- 邮箱: yjin5856@uni.sydney.edu.au
- 微信: A570281374
