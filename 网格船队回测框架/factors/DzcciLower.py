#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff


def signal(*args):
    # DzcciLower
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    tp = (df['high'] + df['low'] + df['close']) / 3.
    _ma = tp.rolling(n, min_periods=1).mean()
    md = (tp - _ma).abs().rolling(n, min_periods=1).mean()
    _cci = (tp - _ma) / (1e-9 + 0.015 * md)
    cci_middle = pd.Series(_cci).rolling(n, min_periods=1).mean()
    cci_lower = cci_middle - 2 * \
        pd.Series(_cci).rolling(n, min_periods=1).std()
    cci_ma = pd.Series(_cci).rolling(max(1, int(n/4)), min_periods=1).mean()

    signal = cci_lower - cci_ma
    df[factor_name] = pd.Series(signal)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

