#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    # PMO 指标
    """

    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['ma'] = df['close'].rolling(n, min_periods=1).mean()
    df['BIAS'] = (df['close'] - df['ma']) / df['ma'] * 100
    df['BIAS_DIF'] = df['BIAS'] - df['BIAS'].shift(3 * n)
    df[factor_name] = df['BIAS_DIF'].rolling(3 * n + 2, min_periods=1).mean()

    del df['ma']
    del df['BIAS']
    del df['BIAS_DIF']


    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df





