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
    # LMA 指标
    """
    N=20
    LMA=MA(LOW,N)
    LMA 为简单移动平均把收盘价替换为最低价。如果最低价上穿/下穿
    LMA 则产生买入/卖出信号。
    """
    df['low_ma'] = df['low'].rolling(n, min_periods=1).mean()
    # 进行去量纲
    df[factor_name] = df['low'] / df['low_ma'] - 1

    del df['low_ma']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df