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

    # SKDJ 指标
    """
    N=60
    M=5
    RSV=(CLOSE-MIN(LOW,N))/(MAX(HIGH,N)-MIN(LOW,N))*100
    MARSV=SMA(RSV,3,1)
    K=SMA(MARSV,3,1)
    D=MA(K,3)
    SKDJ 为慢速随机波动（即慢速 KDJ）。SKDJ 中的 K 即 KDJ 中的 D，
    SKJ 中的 D 即 KDJ 中的 D 取移动平均。其用法与 KDJ 相同。
    当 D<40(处于超卖状态)且 K 上穿 D 时买入，当 D>60（处于超买状
    态）K 下穿 D 时卖出。
    """
    df['RSV'] = (df['close'] - df['low'].rolling(n, min_periods=1).min()) / (df['high'].rolling(n, min_periods=1).max() - df['low'].rolling(n, min_periods=1).min()) * 100
    df['MARSV'] = df['RSV'].ewm(com=2).mean()

    df['K'] = df['MARSV'].ewm(com=2).mean()
    df[factor_name] = df['K'].rolling(3, min_periods=1).mean()
    
    del df['RSV']
    del df['MARSV']
    del df['K']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df