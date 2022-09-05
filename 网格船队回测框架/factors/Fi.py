#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff


def signal(*args):
    # Fi
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    _fi = df['volume'] * (df['close'] - df['close'].shift(1))
    signal = _fi.ewm(span=n, adjust=False, min_periods=1).mean()
    df[factor_name] = pd.Series(signal)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

