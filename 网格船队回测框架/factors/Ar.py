#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff


def signal(*args):

    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    v1 = (df['high'] - df['open']).rolling(n, min_periods=1).sum()
    v2 = (df['open'] - df['low']).rolling(n, min_periods=1).sum()
    _ar = 100 * v1 / v2
    df[factor_name] = pd.Series(_ar)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

