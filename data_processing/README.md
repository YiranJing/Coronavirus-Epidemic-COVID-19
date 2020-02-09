## Daily Data Query from 人民日报


* Reference from repo https://github.com/canghailan/Wuhan-2019-nCoV


### Description

* dataset.py: Utility functions
  * Regional data (DXYArea.csv) contains all the city-level data. Data from Hong Kong SAR, Macao SAR, Tai Wan and Tibet are province-level, not city-level data.
  * Include other countries data
  * The data before 2020-02-07 are collect from other resource



### Usage
See DXY_AreaData_query.ipynb or
```
python DXY_AreaData_query.py # output data (english version in ../data/DXYArea.csv)
```
