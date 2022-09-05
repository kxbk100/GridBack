#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):

    # Demakder 指标
    """
    N=20
    Demax=HIGH-REF(HIGH,1)
    Demax=IF(Demax>0,Demax,0)
    Demin=REF(LOW,1)-LOW
    Demin=IF(Demin>0,Demin,0)
    Demaker=MA(Demax,N)/(MA(Demax,N)+MA(Demin,N))
    当 Demaker>0.7 时上升趋势强烈，当 Demaker<0.3 时下跌趋势强烈。
    当 Demaker 上穿 0.7/下穿 0.3 时产生买入/卖出信号。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['Demax'] = df['high'] - df['high'].shift(1)
    df['Demax'] = np.where(df['Demax'] > 0, df['Demax'], 0)
    df['Demin'] = df['low'].shift(1) - df['low']
    df['Demin'] = np.where(df['Demin'] > 0, df['Demin'], 0)
    df['Demax_ma'] = df['Demax'].rolling(n, min_periods=1).mean()
    df['Demin_ma'] = df['Demin'].rolling(n, min_periods=1).mean()
    df[factor_name] = df['Demax_ma'] / (df['Demax_ma'] + df['Demin_ma'])

    del df['Demax']
    del df['Demin']
    del df['Demax_ma']
    del df['Demin_ma']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
