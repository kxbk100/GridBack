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
    # ZLMACD 指标
    """
    N1=20
    N2=100
    ZLMACD=(2*EMA(CLOSE,N1)-EMA(EMA(CLOSE,N1),N1))-(2*EM
    A(CLOSE,N2)-EMA(EMA(CLOSE,N2),N2))
    ZLMACD 指标是对 MACD 指标的改进，它在计算中使用 DEMA 而不
    是 EMA，可以克服 MACD 指标的滞后性问题。如果 ZLMACD 上穿/
    下穿 0，则产生买入/卖出信号。
    """
    ema1 = df['close'].ewm(n, adjust=False).mean()
    ema_ema_1 = ema1.ewm(n, adjust=False).mean()
    n2 = 5 * n
    ema2 = df['close'].ewm(n2, adjust=False).mean()
    ema_ema_2 = ema2.ewm(n2, adjust=False).mean()
    ZLMACD = (2 * ema1 - ema_ema_1) - (2 * ema2 - ema_ema_2)
    df[factor_name] = df['close'] / ZLMACD - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df