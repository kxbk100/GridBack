#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Pvt 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['PVT'] = (df['close'] - df['close'].shift(1)) / \
        df['close'].shift(1) * df['volume']
    df['PVT_MA'] = df['PVT'].rolling(n, min_periods=1).mean()

    # 去量纲
    df['PVT_SIGNAL'] = (df['PVT'] / df['PVT_MA'] - 1)
    df[factor_name] = df['PVT_SIGNAL'].rolling(n, min_periods=1).sum()

    # 删除多余列
    del df['PVT'], df['PVT_MA'], df['PVT_SIGNAL']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
