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

    df['close_1'] = df['close'].shift()
    tr = df[['high', 'low', 'close_1']].max(
        axis=1) - df[['high', 'low', 'close_1']].min(axis=1)
    atr = tr.rolling(n, min_periods=1).mean()
    df[factor_name] = atr.pct_change(n)

    del df['close_1']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

