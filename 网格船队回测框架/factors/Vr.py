#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff


def signal(*args):
    # Vr
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    av = np.where(df['close'] > df['close'].shift(1), df['volume'], 0)
    bv = np.where(df['close'] < df['close'].shift(1), df['volume'], 0)
    _cv = np.where(df['close'] == df['close'].shift(1), df['volume'], 0)

    avs = pd.Series(av).rolling(n, min_periods=1).sum()
    bvs = pd.Series(bv).rolling(n, min_periods=1).sum()
    cvs = pd.Series(_cv).rolling(n, min_periods=1).sum()

    signal = (avs + 0.5 * cvs) / (1e-9 + bvs + 0.5 * cvs)

    df[factor_name] = pd.Series(signal)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
