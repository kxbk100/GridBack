#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # Rsi_v2
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    close_dif = df['close'].diff()
    df['up'] = np.where(close_dif > 0, close_dif, 0)
    df['down'] = np.where(close_dif < 0, abs(close_dif), 0)
    a = df['up'].rolling(n).sum()
    b = df['down'].rolling(n).sum()
    df[factor_name] = a / (a + b + eps)

    # 删除多余列
    del df['up'], df['down']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
