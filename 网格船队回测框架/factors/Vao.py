#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff, eps

eps = 1e-8


def signal(*args):
    # Vao
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    wv = df['volume'] * (df['close'] - 0.5 * df['high'] - 0.5 * df['low'])
    _vao = wv + wv.shift(1)
    vao_ma1 = _vao.rolling(n, min_periods=1).mean()
    vao_ma2 = _vao.rolling(int(3*n), min_periods=1).mean()

    df[factor_name] = pd.Series(vao_ma1 - vao_ma2)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
