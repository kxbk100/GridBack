#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff, eps


def signal(*args):
    # LongMoment
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    def range_plus(x, np_tmp, rolling_window, lam):
        # 计算滚动到的index
        li = x.index.to_list()
        # 从整块array中截取对应的index的array块
        np_tmp2 = np_tmp[li, :]
        # 按照振幅排序
        np_tmp2 = np_tmp2[np.argsort(np_tmp2[:, 0])]
        # 计算需要切分的个数
        t = int(rolling_window * lam)
        # 计算低价涨跌幅因子
        np_tmp2 = np_tmp2[:t, :]
        s = np_tmp2[:, 1].sum()
        return s

    df['涨跌幅'] = df['close'].pct_change(n)
    # 计算窗口20-180的切割动量与反转因子
    df['振幅'] = (df['high'] / df['low']) - 1
    # 先把需要滚动的两列数据变成array
    np_tmp = df[['振幅', '涨跌幅']].values
    # 计算因子
    df[factor_name] = df['涨跌幅'].rolling(
        n * 10).apply(range_plus, args=(np_tmp, n * 10, 0.7), raw=False)

    del df['振幅'], df['涨跌幅']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
