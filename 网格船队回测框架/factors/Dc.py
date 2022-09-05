#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):

    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # DC 指标
    """
    N=20
    UPPER=MAX(HIGH,N)
    LOWER=MIN(LOW,N)
    MIDDLE=(UPPER+LOWER)/2
    DC 指标用 N 天最高价和 N 天最低价来构造价格变化的上轨和下轨，
    再取其均值作为中轨。当收盘价上穿/下穿中轨时产生买入/卖出信号。
    """
    upper = df['high'].rolling(n, min_periods=1).max()
    lower = df['low'].rolling(n, min_periods=1).min()
    middle = (upper + lower) / 2
    width = upper - lower
    # 进行无量纲处理
    df[factor_name] = width / middle

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
