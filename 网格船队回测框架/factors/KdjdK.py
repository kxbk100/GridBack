#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # KDJD 指标
    """
    N=20
    M=60
    LOW_N=MIN(LOW,N)
    HIGH_N=MAX(HIGH,N)
    Stochastics=(CLOSE-LOW_N)/(HIGH_N-LOW_N)*100
    Stochastics_LOW=MIN(Stochastics,M)
    Stochastics_HIGH=MAX(Stochastics,M)
    Stochastics_DOUBLE=(Stochastics-Stochastics_LOW)/(Stochastics_HIGH-Stochastics_LOW)*100
    K=SMA(Stochastics_DOUBLE,3,1)
    D=SMA(K,3,1)
    KDJD 可以看作 KDJ 的变形。KDJ 计算过程中的变量 Stochastics 用
    来衡量收盘价位于最近 N 天最高价和最低价之间的位置。而 KDJD 计
    算过程中的 Stochastics_DOUBLE 可以用来衡量 Stochastics 在最近
    N 天的 Stochastics 最大值与最小值之间的位置。我们这里将其用作
    动量指标。当 D 上穿 70/下穿 30 时，产生买入/卖出信号。
    """
    min_low = df['low'].rolling(n).min()
    max_high = df['high'].rolling(n).max()
    Stochastics = (df['close'] - min_low) / (max_high - min_low) * 100
    Stochastics_LOW = Stochastics.rolling(n*3).min()
    Stochastics_HIGH = Stochastics.rolling(n*3).max()
    Stochastics_DOUBLE = (Stochastics - Stochastics_LOW) / (Stochastics_HIGH - Stochastics_LOW)
    df[factor_name] = Stochastics_DOUBLE.ewm(com=2).mean() #K
    # df[factor_name] = K.ewm(com=2).mean() #D


    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df


