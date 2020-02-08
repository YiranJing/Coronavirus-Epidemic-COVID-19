## Daily Data Query from DXY


* Original Data from [Ding Xiang Yuan](https://3g.dxy.cn/newh5/view/pneumonia)。
* CSV format data from: https://github.com/BlankerL/DXY-2019-nCoV-Data CSV data file is updated frequently by [2019-nCoV Infection Data Realtime Crawler](https://github.com/BlankerL/DXY-2019-nCoV-Crawler).
* Reference from repo https://github.com/jianxu305/nCov2019_analysis


### Description

* utils.py: Utility functions
  * Regional data (DXYArea.csv) only contains all the city-level data. Data from Hong Kong SAR, Macao SAR, Tai Wan and Tibet are province-level, and not city-level data available from DXY, so they are not in this file.



### Usage
- Choice 1: Terminal:
```sh
$ python DXY_AreaData_query.py # output data in ../data/DXYArea.csv)
```

- Choice 2: Jupyter Notebook `DXY_AreaData_query.ipynb`:
