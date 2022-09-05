#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Cci_v2 最常用的T指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    oma = ta.WMA(df['open'], timeperiod=n)
    hma = ta.WMA(df['high'], timeperiod=n)
    lma = ta.WMA(df['low'], timeperiod=n)
    cma = ta.WMA(df['close'], timeperiod=n)

    tp = (hma + lma + cma + oma) / 4
    ma = ta.WMA(tp, n)
    md = abs(ma - cma).rolling(n, min_periods=1).mean() # MD=MA(ABS(TP-MA),N)
    df[factor_name] = (tp - ma) / (md + eps)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
