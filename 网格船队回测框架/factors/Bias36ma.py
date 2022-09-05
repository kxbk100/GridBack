#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff

def signal(*args):
    # Bias
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    bias36 = df['close'].rolling(3, min_periods=1).mean() - df['close'].rolling(6, min_periods=1).mean()
    df[factor_name] = bias36.rolling(n, min_periods=1).mean()

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
