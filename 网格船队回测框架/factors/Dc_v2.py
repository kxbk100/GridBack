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
    # Dc 指标
    """
    N=20
    UPPER=MAX(HIGH,N)
    LOWER=MIN(LOW,N)
    MIDDLE=(UPPER+LOWER)/2
    Dc 指标用 N 天最高价和 N 天最低价来构造价格变化的上轨和下轨，
    再取其均值作为中轨。当收盘价上穿/下穿中轨时产生买入/卖出信号。
    """
    df[factor_name] = (df['high'].rolling(n, min_periods=1).max() + df['low'].rolling(n, min_periods=1).min()) / 2.

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
