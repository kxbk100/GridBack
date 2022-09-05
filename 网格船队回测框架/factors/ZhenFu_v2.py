#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # ZhenFu_v2
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # 振幅：收盘价、开盘价
    high = df[['close', 'open']].max(axis=1)
    low = df[['close', 'open']].min(axis=1)
    high = pd.Series(high).rolling(n, min_periods=1).max()
    low = pd.Series(low).rolling(n, min_periods=1).min()
    df[factor_name] = high / (low + eps) - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
