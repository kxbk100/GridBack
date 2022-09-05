#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff, eps


def signal(*args):
    # Mm指标
    
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    ma_fast = df['close'].rolling(n, min_periods=1).mean()
    ma_slow = df['close'].rolling(5*n, min_periods=1).mean()
    df[factor_name] = ma_fast / (ma_slow + eps) - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
