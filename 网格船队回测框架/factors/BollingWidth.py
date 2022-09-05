#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Bolling_width 指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['median'] = df['close'].rolling(window=n).mean()
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)
    df['z_score'] = abs(df['close'] - df['median']) / df['std']
    df['m'] = df['z_score'].rolling(window=n).mean()
    df['upper'] = df['median'] + df['std'] * df['m']
    df['lower'] = df['median'] - df['std'] * df['m']
    df[factor_name] = df['std'] * df['m'] * 2 / (df['median'] + eps)

    # 删除多余列
    del df['median'], df['std'], df['z_score'], df['m']
    del df['upper'], df['lower']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
