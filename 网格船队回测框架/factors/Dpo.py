#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff, eps


def signal(*args):
    # Dpo
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['median'] = df['close'].rolling(
        window=n, min_periods=1).mean()  # 计算中轨
    df[factor_name] = (df['close'] - df['median'].shift(int(n / 2) + 1)) / (df['median'] + eps)

    del df['median']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

