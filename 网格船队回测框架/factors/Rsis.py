#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # Rsis
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    close_diff_pos = np.where(df['close'] > df['close'].shift(
        1), df['close'] - df['close'].shift(1), 0)
    rsi_a = pd.Series(close_diff_pos).ewm(
        alpha=1 / (4 * n), adjust=False).mean()
    rsi_b = (df['close'] - df['close'].shift(1)
             ).abs().ewm(alpha=1 / (4 * n), adjust=False).mean()
    rsi = 100 * rsi_a / (eps + rsi_b)
    rsi_min = pd.Series(rsi).rolling(int(4 * n), min_periods=1).min()
    rsi_max = pd.Series(rsi).rolling(int(4 * n), min_periods=1).max()
    rsis = 100 * (rsi - rsi_min) / (eps + rsi_max - rsi_min)
    df[factor_name] = pd.Series(rsis)    

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
