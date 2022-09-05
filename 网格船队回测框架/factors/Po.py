#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):

    # PO指标
    """
    EMA_SHORT=EMA(CLOSE,9)
    EMA_LONG=EMA(CLOSE,26)
    PO=(EMA_SHORT-EMA_LONG)/EMA_LONG*100
    PO 指标求的是短期均线与长期均线之间的变化率。
    如果 PO 上穿 0，则产生买入信号；
    如果 PO 下穿 0，则产生卖出信号。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    ema_short = df['close'].ewm(n, adjust=False).mean()
    ema_long = df['close'].ewm(n * 3, adjust=False).mean()
    df[factor_name] = (ema_short - ema_long) / ema_long * 100

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
