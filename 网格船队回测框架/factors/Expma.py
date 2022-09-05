#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib
from utils.diff import add_diff

# =====函数  01归一化
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)

def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # ******************** Expma ********************
    # N1=12
    # N2=50
    # EMA1=EMA(CLOSE,N1)
    # EMA2=EMA(CLOSE,N2)
    # 指数移动平均是简单移动平均的改进版，用于改善简单移动平均的滞后性问题。
    ema1 = df['close'].ewm(span=n, min_periods=1).mean()
    ema2 = df['close'].ewm(span=(4 * n), min_periods=1).mean()

    signal = ema1 - ema2
    df[factor_name] = scale_01(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df