#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # Rsi_v3
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    diff = df['close'].diff()
    df['up'] = np.where(diff > 0, diff, 0)
    df['down'] = np.where(diff < 0, abs(diff), 0)
    a = df['up'].ewm(span=n).mean()
    b = df['down'].ewm(span=n).mean()
    df[factor_name] = a / (a + b + eps)

    # 删除多余列
    del df['up'], df['down']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
