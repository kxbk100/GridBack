#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Bolling 指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # 计算布林上下轨
    df['std'] = df['close'].rolling(n, min_periods=1).std()
    df['ma'] = df['close'].rolling(n, min_periods=1).mean()
    df['upper'] = df['ma'] + 1.0 * df['std']
    df['lower'] = df['ma'] - 1.0 * df['std']
    df['distance'] = 0
    condition_1 = df['close'] > df['upper']
    condition_2 = df['close'] < df['lower']
    df.loc[condition_1, 'distance'] = df['close'] - df['upper']
    df.loc[condition_2, 'distance'] = df['close'] - df['lower']
    df[factor_name] = df['distance'] / (df['std'] + eps)

    # 删除多余列
    del df['std'], df['ma'], df['upper'], df['lower']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
