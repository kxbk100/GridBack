#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff


def signal(*args):
 # HLMA 指标
    """
    N1=20
    N2=20
    HMA=MA(HIGH,N1)
    LMA=MA(LOW,N2)
    HLMA 指标是把普通的移动平均中的收盘价换为最高价和最低价分
    别得到 HMA 和 LMA。当收盘价上穿 HMA/下穿 LMA 时产生买入/卖
    出信号。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    hma = df['high'].rolling(n, min_periods=1).mean()
    lma = df['low'].rolling(n, min_periods=1).mean()
    df['HLMA'] = hma - lma
    df['HLMA_mean'] = df['HLMA'].rolling(n, min_periods=1).mean()

    # 去量纲
    df[factor_name] = df['HLMA'] / df['HLMA_mean'] - 1

    
    del df['HLMA']
    del df['HLMA_mean']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

