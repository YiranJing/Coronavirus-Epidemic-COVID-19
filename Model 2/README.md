
# Model 2: Simulating Peak of 2019-nCoV in Wuhan after 23 Jan

简体中文 | [English](README.en.md)
***

## Usage:
- Choice 1: Run [Forecast_Outbreak_Wuhan.ipynb](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202/Forecast_Outbreak_Wuhan.ipynb)

- Choice 2:
```sh
pip install -r ../requirements.txt
python run_model2.py
```

***
### More Explanations of the estimated parameters:
1. Estimate the transmission probability (b):
    - `_estimate_transmission_probablity` by `func` in `helper_fun_epi_model.py`:
    - In the beginning (08 Dec 2019), suppose the susceptible group (S) is same as the total population (N). And the number of infected people is 1 (I(t=0) = 1), then apply these condition to SIER model's formula, we get
![](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202/image/model2_formula1.png)

The transmission probability (b) is obtained by resolving the formula above.

2. Estimate `Beta`（β, rate of spread）of SEIR model， and adjust it based on updated new information:
   - **β = kb**, where k is the the number of people a confirmed case contacts/meets daily (感染者平均每天的接触人数)
   - To apply the information of **truth 2**(see below) (i.e. to adjust the rate of spread), what I did is adjust value of k, and keep b as constant.

_If you have further question or suggestions, please create issue or make pull request!_

***
### 模型 2: [模拟预测武汉封城后肺炎感染人数以及峰值](https://github.com/YiranJing/Coronavirus-Epidemic-2019-nCov/blob/master/Model%202)📈
   - 作者: 景怡然
   > Method: Deterministic SEIR (susceptible-exposed-infectious- recovered) model and Sensitivity analysis

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
