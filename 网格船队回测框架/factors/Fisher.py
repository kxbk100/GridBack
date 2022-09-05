#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):

    # FISHER指标
    """
    N=20
    PARAM=0.3
    PRICE=(HIGH+LOW)/2
    PRICE_CH=2*(PRICE-MIN(LOW,N)/(MAX(HIGH,N)-MIN(LOW,N))-
    0.5)
    PRICE_CHANGE=0.999 IF PRICE_CHANGE>0.99 
    PRICE_CHANGE=-0.999 IF PRICE_CHANGE<-0.99
    PRICE_CHANGE=PARAM*PRICE_CH+(1-PARAM)*REF(PRICE_CHANGE,1)
    FISHER=0.5*REF(FISHER,1)+0.5*log((1+PRICE_CHANGE)/(1-PRICE_CHANGE))
    PRICE_CH 用来衡量当前价位于过去 N 天的最高价和最低价之间的
    位置。Fisher Transformation 是一个可以把股价数据变为类似于正态
    分布的方法。Fisher 指标的优点是减少了普通技术指标的滞后性。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    PARAM = 1/ n
    df['price'] = (df['high'] + df['low']) / 2
    df['min_low'] = df['low'].rolling(n).min()
    df['max_high'] = df['high'].rolling(n).max()
    df['price_ch'] = 2 * (df['price'] - df['min_low']) / (df['max_high'] - df['low']) - 0.5
    df['price_change'] = PARAM * df['price_ch'] + (1 - PARAM) * df['price_ch'].shift(1)
    df['price_change'] = np.where(df['price_change'] > 0.99, 0.999, df['price_change'])
    df['price_change'] = np.where(df['price_change'] < -0.99, -0.999, df['price_change'])
    df[factor_name] = 0.5 * np.log((1+df['price_change']) / (1 - df['price_change']))

    del df['price']
    del df['min_low']
    del df['max_high']
    del df['price_ch']
    del df['price_change']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df







