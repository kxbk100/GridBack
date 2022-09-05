#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff

# =====函数  01归一化
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)

def signal(*args):
    # Bias
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    bias36 = df['close'].rolling(3, min_periods=1).mean() - df['close'].rolling(6, min_periods=1).mean()
    bias36_ma = bias36.rolling(n, min_periods=1).mean()

    signal = bias36 - bias36_ma
    df[factor_name] = scale_01(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
