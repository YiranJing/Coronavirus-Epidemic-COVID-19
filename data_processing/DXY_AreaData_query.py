# Query real time data from DingXiangYuan, and keep the latest records every day for each city


#### resource: https://github.com/jianxu305/nCov2019_analysis


import pandas as pd
import matplotlib.pyplot as plt
import utils   # some convenient functions
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


        
def main():
    
    DXYArea = utils.load_chinese_data() # Query latest Regional Data from DXY
    daily_frm_DXYArea = utils.aggDaily(DXYArea)  # aggregate to daily data (keep the latest records every day)
    
    daily_frm_DXYArea.to_csv ('../data/DXYArea.csv', index = None, header=True)
    print("Save area daily dataset (English) into ../data/DXYArea.csv")
    
if __name__ == '__main__':
    main()