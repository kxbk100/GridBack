#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # D
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    low_list = df['low'].rolling(n, min_periods=1).min()  # MIN(LOW,N) 求周期内low的最小值
    high_list = df['high'].rolling(
        n, min_periods=1).max()  # MAX(HIGH,N) 求周期内high 的最大值
    # Stochastics=(CLOSE-LOW_N)/(HIGH_N-LOW_N)*100 计算一个随机值
    rsv = (df['close'] - low_list) / (high_list - low_list + eps) * 100
    # K D J的值在固定的范围内
    df['K'] = rsv.ewm(com=2).mean()  # K=SMA(Stochastics,3,1) 计算k
    df[factor_name] = df['K'].ewm(com=2).mean()  # D=SMA(K,3,1)  计算D

    # 删除多余列
    del df['K']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
