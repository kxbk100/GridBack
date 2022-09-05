#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff

# =====函数  zscore归一化
def scale_zscore(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).mean()
          ) / pd.Series(_s).rolling(_n, min_periods=1).std()
    return pd.Series(_s)

def signal(*args):
    # DzrsiLowerSignal
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    rtn = df['close'].diff()
    up = np.where(rtn > 0, rtn, 0)
    dn = np.where(rtn < 0, rtn.abs(), 0)
    a = pd.Series(up).rolling(n, min_periods=1).sum()
    b = pd.Series(dn).rolling(n, min_periods=1).sum()

    a *= 1e3
    b *= 1e3

    rsi = a / (1e-9 + a + b)

    rsi_middle = rsi.rolling(n, min_periods=1).mean()
    # rsi_upper = rsi_middle + 2 * rsi.rolling(n, min_periods=1).std()
    rsi_lower = rsi_middle - 2 * rsi.rolling(n, min_periods=1).std()
    rsi_ma = rsi.rolling(int(n / 2), min_periods=1).mean()

    signal = rsi_lower - rsi_ma
    df[factor_name] = scale_zscore(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

