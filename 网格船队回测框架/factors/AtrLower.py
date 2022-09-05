#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff, eps


def signal(*args):
    # AtrLower
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    tr = np.max(np.array([
        df['high'] - df['low'],
        (df['high'] - df['close'].shift(1)).abs(),
        (df['low'] - df['close'].shift(1)).abs()
    ]), axis=0)
    atr = pd.Series(tr).rolling(n, min_periods=1).mean()
    _ma = df['close'].rolling(n, min_periods=1).mean()

    dn = _ma - atr * 0.2 * n
    df[factor_name] = dn
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
