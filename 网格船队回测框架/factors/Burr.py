#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff, eps


def signal(*args):
    # Burr
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    # 只在上涨跌时关注回落幅度
    df['scores_high'] = (1 - df['close'] / df['high'].rolling(
        window=n, min_periods=1).max()).where(df['close'] - df['open'].shift(n) > 0)
    # 只在下跌时关注回升幅度
    df['scores_low'] = (1 - df['close'] / df['low'].rolling(
        window=n, min_periods=1).min()).where(df['close'] - df['open'].shift(n) < 0)
    df[factor_name] = df['scores_high'].fillna(
        0) + df['scores_low'].fillna(0)  # [-1, 1]
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
