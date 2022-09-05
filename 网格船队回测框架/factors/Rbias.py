#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Rbias
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    ma = df['close'].rolling(n, min_periods=1).mean()
    df[factor_name] = (df['close'] / ma) / (df['close'].shift(1)/ma.shift(1)) - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
