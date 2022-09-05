#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # 收高差值 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    high = df['high'].rolling(n, min_periods=1).mean()
    close = df['close']
    df[factor_name] = (close - high) / (high + eps)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
