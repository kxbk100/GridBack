#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy  as np
import talib
import pandas as pd
from utils.diff import add_diff

# =====函数  zscore归一化
def scale_zscore(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).mean()
          ) / pd.Series(_s).rolling(_n, min_periods=1).std()
    return pd.Series(_s)

def signal(*args):
    # EnvUpperSignal
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    upper = (1 + 0.05) * df['close'].rolling(n, min_periods=1).mean()

    signal = df['close'] - upper
    df[factor_name] = scale_zscore(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
