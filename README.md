# 估计和预测 2019-nCoV 新型冠状病毒在武汉的爆发情况

简体中文 | [English](README.en.md)

#### 日期: 2020年1月

***

## 项目:
> 2020年1月23日，交通枢纽的武汉市被封城。900万人民被困在武汉市区。在此之前，有500万人因春节离开武汉。估计机场的国际人流量为1900万。

考虑到新型武汉肺炎的快速传播性和武汉居住人口在封城前后变化巨大，我选择了不同的模型来估计封城前后武汉的感染人数，主要参考和借鉴今日发表的相关论文，数据参考官方数据。

#### 以下模型的重要局限：
1. 模型的各种假设对结论的影响非常大。（很难收集到足够准确且全面的信息，所以有些假设未必合适）
   - 每个模型的敏感度测试有针对部分假设做一些调整
2. 以下的模型都非常简单，而且没有包含足够多的数据，所得结论只是粗略估计
   - 但是因为仅针对武汉市区预测，所以或许这么简单的模型就足够了
   - 会根据最新消息持续更新模型

#### 预测未来病情走势困难的主要原因：
1. 我们目前对2019-nCoV的了解还有许多未知
   - 比如，我们不能正确地检测出所有感染患者：约17% 的病患不会表现出明显症状，但是依旧可以传染病毒给他人
2. **我们无法得到真实的历史数据**, 中国官方的数据是低于实际情况的，尤其是武汉市
   - 比如说，封城的时候到底检测出了多少病患，我们无从知晓
3. **官方不断颁布的新政策对病情走势影响很大**
   - 比如，交通限制，强制居家隔离（反而造成大量家庭内部感染），2月5号之后武汉新建立的三所医院开始接受大量病患
   - 这些随着时间发展快速变化的正常都对病情控制有很大的影响。**而当我们用模型预测未来时，我们的重要前提假设是未来不会有新的政策发生**。

***
#### 从丁香园抓取最新数据
```sh
## Update data from DXY
$ cd ../data_processing && python DXY_AreaData_query.py # save data out to data folder.
```
### 模型 1: [估计武汉封城时的感染人数](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)😷
   - 作者: 景怡然
   - **主要结论(_仅仅针对武汉市_)： 截止1月23日，武汉有超过 38500 名感染者加确诊者，95%置信区间(30000, 48470)**，根据1月29号海外发现的感染人数计算，引用2018年的交通数据估算。
   > Method: Considering Wuhan is the major air and train transportation hub of China, we use the number of cases exported from Wuhan internationally as the sample, assuming the infected people follow a Possion distribution, then calculate the 95% confidence interval by profile likelihood method. Sensitivity analysis followed by.

   > Reference: [report2 (Jan 21)](https://www.imperial.ac.uk/media/imperial-college/medicine/sph/ide/gida-fellowships/2019-nCoV-outbreak-report-22-01-2020.pdf)

### 模型 2: [模拟预测武汉封城后肺炎感染人数以及峰值](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202)📈
   - 作者: 景怡然
   > Method: Deterministic SIER (susceptible-exposed-infectious- recovered) model and Sensitivity analysis

   > Reference: [Nowcasting and forecasting the potential domestic and international spread of the 2019-nCoV outbreak (Jan 31)](https://www.thelancet.com/action/showPdf?pii=S0140-6736%2820%2930260-9)

   - **主要结论(_仅仅针对武汉市_):** (根据 2019-12-08 至 2020-02-02 的官方数据)
      - 估计最初的传播速率 **R0** (基本传染数) 为: **2.9**
      - **在非常乐观的情况下，预测武汉肺炎的感染人数会超过 1.4 万人 (非累计，仅峰值)，峰值最早在2月中下旬出现** (峰值为下图的红线最高点); **整个过程直到疫情结束，武汉累计患病总数约为5万** (绿色的线)
      - **实情1**: 考虑到医疗资源不足和官方数据低于实际，武汉肺炎患者的实际峰值可能会在1.6万至2.5万人之间
      - **实情2**: 肺炎传染风险在封城之后，到2月5号之前依旧很高，主要原因是很多病患传染一家人。2月5号之后武汉3所新医院开始投入使用，所以传染风险会有明显下降
        > 根据2月2号官方媒体爆料，患者发现并不及时而且隔离措施也没有做的很好。基于这个现实，武汉肺炎患者的实际峰值很可能超过10万甚至15万。
        > 更新：2月5号之后，武汉新建的三所医院开始收纳病患（共计有6000床位），所以现在的传染风险应该有明显下降，毕竟更多的病人可以被医院收容（治疗/强制隔离）
      - **结合实情1和2，武汉实际肺炎患者人数应该在2.5万至10万之间**
      - 封城措施对控制病情有非常显著的作用: 根据模型估算，如果不封城，仅仅隔离患者，武汉患者峰值可能会高达20万
   - 模型主要假设:
      - 潜伏人群是确诊病例的五倍。(确诊病例按照4109计算，截止2月2日)
      - 23号封城以后，所有确诊病例都会被严格隔离
      - 假设肺炎死亡率为3%（官方数字）
      - 23号之前，平均1个感染者会接触5个人；23号以后，平均1个感染者最多只会接触1个人 (k)
      - 23号之前，武汉人口为1100万；23号后，武汉人口为900万
      - 平均潜伏期为7天，恢复期约为14天
      - 乐观估计医疗资源充足且官方数字准确
![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202/image/withControl.png)

注释:
- Removed(移除人群): 治愈或者死亡
- Death(死亡患者): 移除人群 * 致死率
- Exposed(潜伏人群): 在潜伏期的患者
- Susceptible(易感人群): 健康但有风险被感染的人群
- Infected(确诊并隔离患者): 确诊人群
![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202/image/SIER2.png)

### 敏感度分析测试
#### 测试1: 官方数字低于实际:
  - 用[模型 1](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/tree/master/Model%201)的结论作为初始条件
  - 在1月23号有38500名感染者，假设其中80%在潜伏期，其余为有明显症状患者
  - 假设目前死亡率等于治愈率，均为3% （根据官方数字）
  - **估计武汉患者最多可超过2.2万人 (非累计，仅峰值)**
#### 测试2: 医疗资源不充足
  - 假设恢复期为20天，而不是14天
  - 估计最初的传播速率 R0 (基本传染数) 为: 3.7
  - **估计武汉肺炎的患者会超过 1.6 万人 (非累计，仅峰值)**, 基于官方数字
#### 测试3: 早发现早隔离并不能做的很好
  > 2月2日李兰娟院士在接受新闻采访时说，检测试剂盒供应不足，且部分患者检测结果回呈阴性，所以其实做不到“早发现，早隔离，早诊断，早治疗”
  > 近期不断有媒体爆料称新型肺炎的传播途径多种多样，比传统流行病更加难以预防

  - 假设23号以后，平均1个感染者依旧会传染给2个人
  - **估计武汉肺炎的患者会超过 10 万人 (非累计，仅峰值)**, 基于官方数字  
#### 测试4: 官方数字低于实际+医疗资源不足
  - 假设恢复期为20天
  - 假设在1月23号有38500名感染者，假设其中80%在潜伏期，其余为有明显症状患者
  - **估计武汉肺炎的患者会超过 2.5 万人 (非累计，仅峰值)**
#### 测试5: 官方数字低于实际+医疗资源不足+早发现早隔离并不能做的很好
  - 假设恢复期为20天
  - 假设在1月23号有38500名感染者，假设其中80%在潜伏期，其余为有明显症状患者
  - 假设23号以后，平均1个感染者依旧会传染给2个人
  - **估计武汉肺炎的患者会高达 15 万人 (非累计，仅峰值)**

## 可视化
[CoronaTracker Analytics Dashboard](https://www.coronatracker.com/analytics/)

***
### To do
我在2月4号加入 [CoronaTracker](https://www.coronatracker.com/)的分析小组，我们目前的分析项目内容包括：
- Latest Stats
- News Aggregator
- Health advisories
- Health-center locators
- Geomap+Travel-path of disease
- Baseline Mortality Estimations
- Topic modelling + Sentiment
[安卓版app下载链接](https://play.google.com/store/apps/details?id=com.coronatracker.corona_flutter&hl=en_AU)

目前关于肺炎的学习和任务，以及接下来的方向在这里更新：[Project](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/projects/1)

如果你对肺炎相关的数据分析和可视化感兴趣，请联系我！

- 邮箱: yjin5856@uni.sydney.edu.au
- 微信: A570281374
