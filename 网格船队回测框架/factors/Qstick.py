#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):

    # Qstick 指标
    """
    N=20
    Qstick=MA(CLOSE-OPEN,N)
    Qstick 通过比较收盘价与开盘价来反映股价趋势的方向和强度。如果
    Qstick 上穿/下穿 0 则产生买入/卖出信号。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    cl = df['close'] - df['open']
    Qstick = cl.rolling(n, min_periods=1).mean()
    # 进行无量纲处理
    df[factor_name] = cl / Qstick - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
