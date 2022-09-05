#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff,eps


def signal(*args):
    # Rwi
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    tr = np.max(np.array([
                (df['high'] - df['low']).abs(),
                (df['high'] - df['close'].shift(1)).abs(),
                (df['close'].shift(1) - df['low']).abs()
                ]), axis=0)  # 三个数列取其大值

    atr = pd.Series(tr).rolling(n, min_periods=1).mean()
    _rwih = (df['high'] - df['low'].shift(1)) / (np.sqrt(n) * atr)
    _rwil = (df['high'].shift(1) - df['low']) / (np.sqrt(n) * atr)

    _rwi = (df['close'] - _rwil) / (1e-9 + _rwih - _rwil)
    df[factor_name] = pd.Series(_rwi)
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
