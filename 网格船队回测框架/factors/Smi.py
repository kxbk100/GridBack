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
    # SMI 指标
    """
    N1=20
    N2=20
    N3=20
    M=(MAX(HIGH,N1)+MIN(LOW,N1))/2
    D=CLOSE-M
    DS=EMA(EMA(D,N2),N2)
    DHL=EMA(EMA(MAX(HIGH,N1)-MIN(LOW,N1),N2),N2)
    SMI=100*DS/DHL
    SMIMA=MA(SMI,N3)
    SMI 指标可以看作 KDJ 指标的变形。不同的是，KD 指标衡量的是当
    天收盘价位于最近 N 天的最高价和最低价之间的位置，而 SMI 指标
    是衡量当天收盘价与最近 N 天的最高价与最低价均值之间的距离。我
    们用 SMI 指标上穿/下穿其均线产生买入/卖出信号。
    """
    df['max_high'] = df['high'].rolling(n, min_periods=1).mean()
    df['min_low'] = df['low'].rolling(n, min_periods=1).mean()
    df['M'] = (df['max_high'] + df['min_low']) / 2
    df['D'] = df['close'] - df['M']
    df['ema'] = df['D'].ewm(n, adjust=False).mean()
    df['DS'] = df['ema'].ewm(n, adjust=False).mean()
    df['HL'] = df['max_high'] - df['min_low']
    df['ema_hl'] = df['HL'].ewm(n, adjust=False).mean()
    df['DHL'] = df['ema_hl'].ewm(n, adjust=False).mean()
    df['SMI'] = 100 * df['DS'] / df['DHL']
    df[factor_name] = df['SMI'].rolling(n, min_periods=1).mean()

    del df['max_high']
    del df['min_low']
    del df['M']
    del df['D']
    del df['ema']
    del df['DS']
    del df['HL']
    del df['ema_hl']
    del df['DHL']
    del df['SMI']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df




