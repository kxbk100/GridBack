#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    short_windows = n
    long_windows = 3 * n
    df['ema_short'] = df['close'].ewm(span=short_windows, adjust=False).mean()
    df['ema_long'] = df['close'].ewm(span=long_windows, adjust=False).mean()
    df['diff_ema'] = df['ema_short'] - df['ema_long']

    df['diff_ema_mean'] = df['diff_ema'].ewm(span=n, adjust=False).mean()

    df[factor_name] = df['diff_ema'] / df['diff_ema_mean'] - 1
    
    del df['ema_short']
    del df['ema_long']
    del df['diff_ema']
    del df['diff_ema_mean']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df