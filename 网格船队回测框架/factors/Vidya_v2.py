#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff


def signal(*args):
    # Vidya_v2
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    _ts = (df['open'] + df['close']) / 2.

    _vi = (_ts - _ts.shift(n)).abs() / (
        _ts - _ts.shift(1)).abs().rolling(n, min_periods=1).sum()
    _vidya = _vi * _ts + (1 - _vi) * _ts.shift(1)

    df[factor_name] = pd.Series(_vidya)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
