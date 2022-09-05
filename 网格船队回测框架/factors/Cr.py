#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff


def signal(*args):
    # Cr
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    _typ = (df['high'] + df['low'] + df['close']) / 3
    _h = np.maximum(df['high'] - pd.Series(_typ).shift(1), 0)  # 两个数列取大值
    _l = np.maximum(pd.Series(_typ).shift(1) - df['low'], 0)

    signal = 100 * pd.Series(_h).rolling(n, min_periods=1).sum() / (
        1e-9 + pd.Series(_l).rolling(n, min_periods=1).sum())
    df[factor_name] = pd.Series(signal)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

