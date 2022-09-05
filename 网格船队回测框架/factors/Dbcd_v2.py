#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    # Dbcd_v2 指标
    """

    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    close_s = df['close']
    ma = close_s.rolling(n, min_periods=1).mean()
    bias = 100 * (close_s - ma) / ma
    bias_dif = bias - bias.shift(int(3 * n + 1))
    _dbcd = bias_dif.ewm(alpha=1 / (3 * n + 2), adjust=False).mean()
    df[factor_name] = pd.Series(_dbcd)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df





