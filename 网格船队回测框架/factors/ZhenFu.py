#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # ZhenFu
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    high = df['high'].rolling(n, min_periods=1).max()
    low = df['low'].rolling(n, min_periods=1).min()
    df[factor_name] = high / (low + eps) - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
