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
    # TYP 指标
    """
    N1=10
    N2=30
    TYP=(CLOSE+HIGH+LOW)/3
    TYPMA1=EMA(TYP,N1)
    TYPMA2=EMA(TYP,N2)
    在技术分析中，典型价格（最高价+最低价+收盘价）/3 经常被用来代
    替收盘价。比如我们在利用均线交叉产生交易信号时，就可以用典型
    价格的均线。
    TYPMA1 上穿/下穿 TYPMA2 时产生买入/卖出信号。
    """
    TYP = (df['close'] + df['high'] + df['low']) / 3
    TYPMA1 = TYP.ewm(n, adjust=False).mean()
    TYPMA2 = TYP.ewm(n * 3, adjust=False).mean()
    diff_TYP = TYPMA1 - TYPMA2
    diff_TYP_mean = diff_TYP.rolling(n, min_periods=1).mean()
    diff_TYP_std = diff_TYP.rolling(n, min_periods=1).std()

    # 无量纲
    df[factor_name] = diff_TYP - diff_TYP_mean / diff_TYP_std

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df