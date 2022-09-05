#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff


def signal(*args):
    # Emv
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    mpm = (df['high'] + df['low']) / 2. - \
        (df['high'].shift(1) + df['low'].shift(1)) / 2.
    v_divisor = df['volume'].rolling(n, min_periods=1).mean()
    _br = df['volume'] / v_divisor / (1e-9 + df['high'] - df['low'])

    signal = mpm / (1e-9 + _br)
    df[factor_name] = pd.Series(signal)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

