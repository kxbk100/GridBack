"""
花式网格船队 第2期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
import os
import pandas as pd
from joblib import Parallel, delayed

csv_path = '/Users/yanjichao/develop/quant/history_candle_data/binance/swap/swap_1m/'  # 读取CSV文件的路径
pkl_path = '/Users/yanjichao/develop/quant/history_candle_data/binance/swap/swap_1m_pkl'  # 保存PKL文件的路径，要用pkl文件还要修改config里面的candle_path

file_list = os.listdir(csv_path)
file_list = [f for f in file_list if '.csv' in f]


# 将csv文件保存为pkl文件，可以加快后续回测速度
def csv2pkl(file):
    print(file)
    df = pd.read_csv(os.path.join(csv_path, file), encoding='gbk', parse_dates=['candle_begin_time'], skiprows=1)
    df.to_pickle(os.path.join(pkl_path, file.replace('csv', 'pkl')))


# 使用多进程
Parallel(n_jobs=max(os.cpu_count() - 1, 1))(
    delayed(csv2pkl)(file)
    for file in file_list
)
