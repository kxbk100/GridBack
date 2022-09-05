#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff


def signal(*args):
    # GAP 常用的T指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['_ma'] = df['close'].rolling(window=n, min_periods=1).mean()
    df['_wma'] = ta.WMA(df['close'], n)
    df['_gap'] = df['_wma'] - df['_ma']
    df[factor_name] = (df['_gap'] / abs(df['_gap']).rolling(window=n).sum())

    del df['_ma']
    del df['_wma']
    del df['_gap']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
