#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Kpower 指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['k_power'] = (df['close'] - df['open'])/df['avg_price'] * 0.6 + 0.2 * (
        df[['close', 'open']].min(axis=1) - df['low'])/df['avg_price'] - 0.2 * (
        df['high'] - df[['close', 'open']].max(axis=1))/df['avg_price']
    df[factor_name] = df['k_power'].rolling(window=n).sum()

    # 删除多余列
    del df['k_power']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
