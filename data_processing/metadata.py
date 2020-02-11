import re
from functools import lru_cache
import pandas as pd
import pandas
import datetime
import matplotlib.pyplot as plt


# 加载静态数据
country_code = pd.read_csv("CountryCode.csv")
china_area_code = pd.read_csv("ChinaAreaCode.csv")
china_area_code["code"] = china_area_code["code"].astype(str)
china_area_code["is_province"] = china_area_code["code"].map(
    lambda x: bool(re.match("\\d{2}0000$", x)))
china_area_code["province_code"] = china_area_code["code"].map(
    lambda x: re.sub("\\d{4}$", "0000", x))


@lru_cache(maxsize=128)
def get_country_code(name):
    result = country_code.loc[country_code["name"].isin([name])]["code"]
    if (len(result.values) > 0):
        return result.values[0]
    return ""


@lru_cache(maxsize=64)
def get_china_province_code(name):
    if not name:
        return ""
    result = china_area_code.loc[china_area_code["is_province"] & china_area_code["name"].str.contains(name)]["code"]
    if (len(result.values) > 0):
        return result.values[0]
    return ""


@lru_cache(maxsize=1024)
def get_china_city_code(province_code, name):
    if not name or not province_code:
        return ""
    result = china_area_code.loc[china_area_code["province_code"].isin([province_code]) & ~china_area_code["is_province"] & china_area_code["name"].str.contains(name)]["code"]
    if (len(result.values) > 0):
        return result.values[0]

    for i in range(1, len(name)):
        fuzzy_name = name[:-i] + ".*" + ".*".join(name[-i:])
        result = china_area_code.loc[china_area_code["province_code"].isin([province_code]) & ~china_area_code["is_province"] & china_area_code["name"].str.match(fuzzy_name)]["code"]
        if (len(result.values) > 0):
            # print(f"""{province_code} {fuzzy_name} -> {",".join(result.values)}""")
            return result.values[0]

    return ""


@lru_cache(maxsize=1024)
def get_china_area_name(code, name):
    if not code:
        return name
    result = china_area_code.loc[china_area_code["code"].isin([code])]["name"]
    if (len(result.values) > 0):
        return result.values[0]
    return name

##########################
## Other helper function
##########################


def test_confirm_monotone_increase(df):
    """check if confimed case is monotone increasing """
    city_list = df['city'].unique()
    for city in city_list[1:]:
        sub_df = df[df['city'] == city]
        if not sub_df['confirmed'].is_monotonic:
            #print("The confirmed cases is not monotone increase in city {}".format(city))
            draw_city_trend(city, df) # city 


def add_days(DXYArea: pandas.core.frame.DataFrame) -> pandas.core.frame.DataFrame:
    """
    Create a new column: Days, number of days after 2019-12-08 (detect the first case)
    """
    DXYArea['date'] = pd.to_datetime(DXYArea['date'])
    first_day = datetime.datetime(2019, 12, 8) # the time when detected the first case (2019-12-08)
    DXYArea['Days'] = (DXYArea['date'] - first_day).dt.days
    return DXYArea

def tsplot_conf_dead_cured(df, title_prefix, figsize=(13,10), fontsize=18, logy=False):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    plot_df = df.groupby('date').agg('sum')
    plot_df.plot(y=['confirmed'], style='-*', ax=ax1, grid=True, figsize=figsize, logy=logy, color='black', marker='o')
    if logy:
        ax1.set_ylabel("log(confirmed)", color="black", fontsize=14)
    else:
        ax1.set_ylabel("confirmed", color="black", fontsize=14)
    if 'dailyNew_confirmed' in df.columns:
        ax11 = ax1.twinx()
        ax11.bar(x=plot_df.index, height=plot_df['dailyNew_confirmed'], alpha=0.3, color='blue')
        ax11.set_ylabel('dailyNew_confirmed', color='blue', fontsize=14)
    ax2 = fig.add_subplot(212)
    plot_df.plot(y=['dead', 'cured'], style=':*', grid=True, ax=ax2, figsize=figsize, sharex=False, logy=logy)
    ax2.set_ylabel("count")
    title = title_prefix + ' Cumulative Confirmed, Death, Cure'
    fig.suptitle(title, fontsize=fontsize)
    
def draw_province_trend(title_prefix: str, df: pandas.core.frame.DataFrame):
    """
    df is the daily dataset from DXY
    """
    sub_df = df[df['province'] == title_prefix]
    tsplot_conf_dead_cured(sub_df, title_prefix)
    
def draw_city_trend(title_prefix: str, df: pandas.core.frame.DataFrame):
    """
    df is the daily dataset from DXY
    """
    sub_df = df[df['city'] == title_prefix]
    tsplot_conf_dead_cured(sub_df, title_prefix)
