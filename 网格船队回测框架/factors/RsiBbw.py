#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff, eps


def signal(*args):
    # RsiBbw指标
    
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    close_dif = df['close'].diff()
    df['up'] = np.where(close_dif > 0, close_dif, 0)
    df['down'] = np.where(close_dif < 0, abs(close_dif), 0)
    a = df['up'].rolling(n).sum()
    b = df['down'].rolling(n).sum()
    df['rsi'] = (a / (a+b+eps)) * 100
    df['median'] = df['close'].rolling(n, min_periods=1).mean()
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)
    df['bbw'] = (df['std'] / df['median']).diff(n)
    df[factor_name] = (df['bbw']) * (df['close'] / df['close'].shift(n) - 1) * df['rsi']

    del df['up'], df['down'], df['rsi'], df['median'], df['std'], df['bbw']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
