#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff


def signal(*args):
    # PjcDistance指标
    
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # 计算均线
    df['median'] = df['close'].rolling(n, min_periods=1).mean()
    # 计算每根k线收盘价和均线的差值，取绝对数
    df['cha'] = abs(df['close'] - df['median'])
    # 计算平均差
    df['ping_jun_cha'] = df['cha'].rolling(n, min_periods=1).mean()

    # 将收盘价小于平均差的偏移量设置为0
    condition_0 = df['close'] <= df['ping_jun_cha']
    condition_1 = df['close'] > df['ping_jun_cha']
    df.loc[condition_0, 'distance'] = 0
    df.loc[condition_1, 'distance'] = df['close'] - df['ping_jun_cha']

    # 计算收盘价相对平均差的偏移比例
    df[factor_name] = (df['distance'] / df['ping_jun_cha']) - 1

    del df['median'], df['cha'], df['ping_jun_cha'], df['distance']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
