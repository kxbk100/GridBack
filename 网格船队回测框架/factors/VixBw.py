#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):

    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    """

    """
    df['vix'] = df['close'] / df['close'].shift(n) - 1
    df['vix_median'] = df['vix'].rolling(
        window=n, min_periods=1).mean()
    df['vix_std'] = df['vix'].rolling(n, min_periods=1).std()
    df['vix_score'] = abs(
        df['vix'] - df['vix_median']) / df['vix_std']
    df['max'] = df['vix_score'].rolling(
        window=n, min_periods=1).mean().shift(1)
    df['min'] = df['vix_score'].rolling(
        window=n, min_periods=1).min().shift(1)
    df['vix_upper'] = df['vix_median'] + df['max'] * df['vix_std']
    df['vix_lower'] = df['vix_median'] - df['max'] * df['vix_std']
    df[factor_name] = (
                                   df['vix_upper'] - df['vix_lower']) * np.sign(df['vix_median'].diff(n))
    condition1 = np.sign(df['vix_median'].diff(
        n)) != np.sign(df['vix_median'].diff(1))
    condition2 = np.sign(df['vix_median'].diff(
        n)) != np.sign(df['vix_median'].diff(1).shift(1))
    df.loc[condition1, factor_name] = 0
    df.loc[condition2, factor_name] = 0
    # ATR指标去量纲



    del df['vix']
    del df['vix_median']
    del df['vix_std']
    del df['max']
    del df['min']
    del df['vix_upper'],df['vix_lower']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

