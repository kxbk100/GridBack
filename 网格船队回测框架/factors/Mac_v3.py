#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    # ********************均线收缩********************

    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    high = df['high'].rolling(n, min_periods=1).max()
    low = df['low'].rolling(n, min_periods=1).min()

    ma_short = (0.5 * high + 0.5 * low).rolling(n, min_periods=1).mean()
    ma_long = (0.5 * high + 0.5 * low).rolling(2 * n, min_periods=1).mean()

    df[factor_name] = 10 * (ma_short - ma_long)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df