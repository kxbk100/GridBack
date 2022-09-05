#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff


def signal(*args):
    # Ic
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    high_max1 = df['high'].rolling(n, min_periods=1).max()
    high_max2 = df['high'].rolling(int(2 * n), min_periods=1).max()
    high_max3 = df['high'].rolling(int(3 * n), min_periods=1).max()
    low_min1 = df['low'].rolling(n, min_periods=1).min()
    low_min2 = df['low'].rolling(int(2 * n), min_periods=1).min()
    low_min3 = df['low'].rolling(int(3 * n), min_periods=1).min()
    ts = (high_max1 + low_min1) / 2.
    ks = (high_max2 + low_min2) / 2.
    span_a = (ts + ks) / 2.
    span_b = (high_max3 + low_min3) / 2.
    signal = (df['close'] - span_b) / (1e-9 + span_a - span_b)

    df[factor_name] = pd.Series(signal)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

