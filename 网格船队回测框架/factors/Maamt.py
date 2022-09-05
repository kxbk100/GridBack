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

    # MAAMT 指标
    """
    N=40
    MAAMT=MA(AMOUNT,N)
    MAAMT 是成交额的移动平均线。当成交额上穿/下穿移动平均线时产
    生买入/卖出信号。
    """
    df[factor_name] = df['volume'].rolling(n, min_periods=1).mean()

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df