#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # HmaSignal 指标
    """
    N=20
    HmaSignal=MA(HIGH,N)
    HmaSignal 指标为简单移动平均线把收盘价替换为最高价。当最高价上穿/
    下穿 HmaSignal 时产生买入/卖出信号。
    """
    hma = df['high'].rolling(n, min_periods=1).mean()
    df[factor_name] = df['high'] - hma

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df