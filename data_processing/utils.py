## translate into English

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as mfm
import os


_DXY_DATA_PATH_ = 'https://raw.githubusercontent.com/BlankerL/DXY-2019-nCoV-Data/master/csv/DXYArea.csv'
_CHN_FONT_ = None
_FONT_PROP_ = None

def set_font(font_file):
    if not os.path.exists(font_file):
        print(font_file + " not found.  If you wish to display Chinese characters in plots, please use set_font() to set the path to the font file.")
    else:
        global _CHN_FONT_, _FONT_PROP_
        _CHN_FONT_ = font_file
        _FONT_PROP_ = mfm.FontProperties(fname=_CHN_FONT_)
    return
        


def use_chn():
    return _CHN_FONT_ is None


def load_chinese_data():
    data = pd.read_csv(_DXY_DATA_PATH_)
    data['updateTime'] = pd.to_datetime(data['updateTime'])  # original type of updateTime after read_csv is 'str'
    data['updateDate'] = data['updateTime'].dt.date    # add date for daily aggregation
    # display basic info
    print('Latest Update Time: ', data['updateTime'].max())
    print('Data Range: ', data['updateDate'].min(), 'to', data['updateDate'].max())
    print('Data Size: ', data.shape[0])
    return data


def aggDaily(df, clean_data=True):
    '''Aggregate the frequent time series data into a daily frame, ie, one entry per (date, province, city)'''
    frm_list = []
    drop_cols = ['province_' + field for field in ['confirmedCount', 'suspectedCount', 'curedCount', 'deadCount']]  # these can be computed later
    for key, frm in df.drop(columns=drop_cols).sort_values(['updateDate']).groupby(['cityName', 'updateDate']):
        frm_list.append(frm.sort_values(['updateTime'])[-1:])    # take the lastest row within (city, date)
    out = pd.concat(frm_list).sort_values(['updateDate', 'provinceName', 'cityName'])
    to_names = [field for field in ['confirmed', 'suspected', 'cured', 'dead']]
    out = out.rename(columns=dict([('city_' + d + 'Count', d) for d in to_names])).drop(columns=['suspected'])   # the suspected column from csv is not reliable
    if clean_data:
        out = clean(out)
    return out


def clean(df):
    '''
    On some dates, very little provinces have reports (usually happens when just pass mid-night)
    Remove these dates for now.  When I have time, I can fill in previous value
    '''
    province_count_frm = df.groupby('updateDate').agg({'provinceName': pd.Series.nunique})
    invalid_dates = province_count_frm[province_count_frm['provinceName'] < 25].index  # 
    if len(invalid_dates) > 0:
        print("The following dates are removed due to insufficient provinces reported: ", invalid_dates.to_numpy())
    return df[~df['updateDate'].isin(invalid_dates)]
    

def add_dailyNew(df):
    cols = ['confirmed', 'dead', 'cured']
    daily_new = df.groupby('cityName').agg(dict([(n, 'diff') for n in cols]))
    daily_new = daily_new.rename(columns=dict([(n, 'dailyNew_' + n) for n in cols]))
    df = pd.concat([df, daily_new], axis=1, join='outer')
    return df
    
    
def tsplot_conf_dead_cured(df, title_prefix, figsize=(13,6), fontsize=18, logy=False):
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    plot_df = df.groupby('updateDate').agg('sum')
    plot_df.plot(y=['confirmed'], style='-*', grid=True, ax=ax1, figsize=figsize, logy=logy)
    ax2 = fig.add_subplot(212)
    plot_df.plot(y=['dead', 'cured'], style=':*', grid=True, ax=ax2, figsize=figsize, sharex=True, logy=logy)
    title = title_prefix + '累计确诊、死亡、治愈人数'
    if logy:
        title += '（指数）'
    fig.suptitle(title, fontproperties=_FONT_PROP_, fontsize=fontsize)
    return fig


def cross_sectional_bar(df, date_str, col, title='', groupby='provinceName', figsize=(13, 10), fontsize=15):
    date = pd.to_datetime(date_str)
    df_date = df[df['updateDate'] == date]
    group_frm = df_date.groupby(groupby).agg('sum').sort_values(by=col, ascending=True)
    ax = group_frm.plot.barh(y=col, grid=True, figsize=figsize)
    ax.set_yticklabels(group_frm.index, fontproperties=_FONT_PROP_) 
    ax.set_title(date_str + '  ' + title, fontproperties=_FONT_PROP_, fontsize=fontsize)
    ax.legend(loc='lower right')
    return ax
    
    