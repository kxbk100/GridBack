#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # ZhenFuBull
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    high = df[['close', 'open']].max(axis=1)
    low = df[['close', 'open']].min(axis=1)
    high = high.rolling(n, min_periods=1).max()
    high = high.shift(1)
    low = low.rolling(n, min_periods=1).min()
    low = low.shift(1)
    df[factor_name] = (df['close'] - high) / (df['close'] + eps)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
