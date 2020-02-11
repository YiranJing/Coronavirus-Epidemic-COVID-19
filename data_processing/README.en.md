## Real-time data query and save to csv

[简体中文](README.md) | English
* Reference from repo https://github.com/canghailan/Wuhan-2019-nCoV


### Description

* dataset.py: Utility functions
  * Regional data (``..\data\DXYArea.csv`) contains all the city-level data. Data from Hong Kong SAR, Macao SAR, Tai Wan and Tibet are province-level, not city-level data.
  * Include data of other countries.
  * The data **before 2020-02-07** are collect from other resource (published paper and the official report of CCDI). The data after 2020-02-07 are real-time query from https://i.snssdk.com/forum/home/v1/info/?forum_id=1656784762444839.
  * The number of `province total` is when city is None. see `get_province_df` function below
  * The number of `China total` is when province is None. see `get_province_df` function below. **Suggest using data after 2020-01-14**.

* The sum of all cities within one province might slightly different from the total number of the province.
  * If so, trust province-level data.
  * Because time-delay or unknown region resource.

* The `confirmed cases` is cumulative number, including both death or healed cases. So it shouldn't decrease. However, there are some cities or provinces have decreased confirmed cases in some time point, based on the _real time query_ result, to see the detailed cases, please open and run **`Incorrect_confirmed_cases.ipynb`**.
  * Based on the plots inside `Incorrect_confirmed_cases.ipynb`, the data looks correct after 01 Feb 2020. (China's governmemnt made adjustments, mainly in city-level before 07 Feb)

* Added columns:
  * `net_confirmed` = confirmed - cured - dead
  * `Days`: number of days after 2019-12-08 (detect the first case)

### Usage
See `DXY_AreaData_query.ipynb` or
```sh
# get English version dataset
$ python DXY_AreaData_query.py # output data (English version in ../data/DXYArea.csv)

# get Chinese version dataset
$ python dataset.py # output data (Chinese version in ../data/DXYArea_chinese.csv)
```

To get the province data, or China total:
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
