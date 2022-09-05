#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
from utils.diff import add_diff


def signal(*args):
    # CCI 最常用的T指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['tp'] = (df['high'] + df['low'] + df['close']) / 3
    df['ma'] = df['tp'].rolling(window=n, min_periods=1).mean()
    df['md'] = abs(df['close'] - df['ma']).rolling(window=n, min_periods=1).mean()
    df[factor_name] = (df['tp'] - df['ma']) / df['md'] / 0.015

    del df['tp']
    del df['ma']
    del df['md']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
