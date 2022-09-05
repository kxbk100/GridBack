#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # MtmMax 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['mtm'] = df['close'] / df['close'].shift(n) - 1
    df['up'] = df['mtm'].rolling(window=n).max().shift(1)
    df[factor_name] = df['mtm'] - df['up']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
