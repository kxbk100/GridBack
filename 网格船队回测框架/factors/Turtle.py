#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Turtle 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # 计算海龟
    df['open_close_high'] = df[['open', 'close']].max(axis=1)
    df['open_close_low'] = df[['open', 'close']].min(axis=1)
    # 计算atr
    df['c1'] = df['high'] - df['low']
    df['c2'] = abs(df['high'] - df['close'].shift(1))
    df['c3'] = abs(df['low'] - df['close'].shift(1))
    # 计算上下轨
    df['up'] = df['open_close_high'].rolling(
        window=n, min_periods=1).max().shift(1)
    df['dn'] = df['open_close_low'].rolling(
        window=n, min_periods=1).min().shift(1)
    # 计算std
    df['std'] = df['close'].rolling(n, min_periods=1).std()
    # 计算atr
    df['tr'] = df[['c1', 'c2', 'c3']].max(axis=1)
    df['atr'] = df['tr'].rolling(window=n).mean()
    # 将上下轨中间的部分设为0
    condition_0 = (df['close'] <= df['up']) & (df['close'] >= df['dn'])
    condition_1 = df['close'] > df['up']
    condition_2 = df['close'] < df['dn']
    df.loc[condition_0, 'd'] = 0
    df.loc[condition_1, 'd'] = df['close'] - df['up']
    df.loc[condition_2, 'd'] = df['close'] - df['dn']
    df[factor_name] = df['d'] / (df['up'] - df['dn'] + eps)

    del df['up'], df['dn'], df['std'], df['tr'], df['atr'], df['d']
    del df['open_close_high'], df['open_close_low']
    del df['c1'], df['c2'], df['c3']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
