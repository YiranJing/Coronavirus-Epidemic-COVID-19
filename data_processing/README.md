## 实时数据抓取并储存在csv

简体中文 | [English](README.en.md)

* 代码来源 https://github.com/canghailan/Wuhan-2019-nCoV


### 数据描述
* dataset.py: Utility functions
  * 地区数据
     * `..\data\DXYArea.csv` 为英文版
     * `..\data\DXYArea_chinese.csv` 为中文版
     * 包括所有城市级数据。上海北京香港台湾澳门数据为省级，而不是市级
     * 包括其他国家数据
     * **2020-02-7之前** 的数据是从其他地方收集的：发表的论文，中央纪检委官方报告等。**2020-02-7之后** 的数据是从数据借口https://i.snssdk.com/forum/home/v1/info/?forum_id=1656784762444839实时抓取
     * `省级总和`是当`city`为none的时候，详情请看下面`get_province_df` function
     * `国家总和`是当`province` 为none的时候，详请请看下面`get_province_df` function。**建议使用2020-01-14之后的数据建模**
* 省级总和的数据可能不等于所有市加和。如果这样的话，以省级数据为准。错误原因可能是时间延迟或未知区域的数据报出。

* 确诊人数`confirmed cases` 是累计总和，包括了死亡和治愈病例。所以这个数字不应该下降。
     * 但是数据结果里的确有一些市或省确诊人数在个别时间点有下降，但是变化不是很大，城市以及错误情况请打开并运行`Incorrect_confirmed_cases.ipynb`。从这里面的图标看，2月1号之后的数据基本都比较正确。（国家在2月7号有对数据做从新调整）

* 额外添加的列（仅在`..\data\DXYArea.csv`):
     * `net_confirmed`（净确诊人数）: = confirmed - cured - dead
     * `Days`: number of days after 2019-12-08 (detect the first case)

### Usage
See `DXY_AreaData_query.ipynb` or
```sh
# get English version dataset
$ python DXY_AreaData_query.py # output data (English version in ../data/DXYArea.csv)

# get Chinese version dataset
$ python dataset.py # output data (Chinese version in ../data/DXYArea_chinese.csv)
```

To get the 省级总和, or 国家总和:
```python
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
```
