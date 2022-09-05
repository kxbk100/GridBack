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
    # IMI 指标
    """
    N=14
    INC=SUM(IF(CLOSE>OPEN,CLOSE-OPEN,0),N)
    DEC=SUM(IF(OPEN>CLOSE,OPEN-CLOSE,0),N)
    IMI=INC/(INC+DEC)
    IMI 的计算方法与 RSI 很相似。其区别在于，在 IMI 计算过程中使用
    的是收盘价和开盘价，而 RSI 使用的是收盘价和前一天的收盘价。所
    以，RSI 做的是前后两天的比较，而 IMI 做的是同一个交易日内的比
    较。如果 IMI 上穿 80，则产生买入信号；如果 IMI 下穿 20，则产生
    卖出信号。
    """
    df['INC'] = np.where(df['close'] > df['open'], df['close'] - df['open'], 0)
    df['INC_sum'] = df['INC'].rolling(n).sum()
    df['DEC'] = np.where(df['open'] > df['close'], df['open'] - df['close'], 0)
    df['DEC_sum'] = df['DEC'].rolling(n).sum()
    df[factor_name] = df['INC_sum'] / (df['INC_sum'] + df['DEC_sum'])

    
    del df['INC']
    del df['INC_sum']
    del df['DEC']
    del df['DEC_sum']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df