#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Bolling_v2 指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['median'] = df['close'].rolling(n, min_periods=1).mean()
    df['std'] = df['close'].rolling(n).std(ddof=0)
    df['upper'] = df['median'] + 0.5 * df['std']
    df['lower'] = df['median'] - 0.5 * df['std']
    df[factor_name] = (df['upper'] - df['lower']) / (df['median'] + eps)

    # 删除多余列
    del df['median'], df['std'], df['upper'], df['lower']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
