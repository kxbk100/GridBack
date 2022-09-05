#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # Bias_v4   
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    ts = df[['high', 'low', 'close']].sum(axis=1) / 3.
    ma = ts.rolling(n, min_periods=1).mean()
    df[factor_name] = ts / (ma + eps) - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
