#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # AvgPrice
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['price'] = df['quote_volume'].rolling(n, min_periods=1).sum() / df['volume'].rolling(n, min_periods=1).sum()
    df[factor_name] = (df['price'] - df['price'].rolling(n, min_periods=1).min()) / (
        df['price'].rolling(n, min_periods=1).max() - df['price'].rolling(n, min_periods=1).min() + eps)

    # 删除多余列
    del df['price']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
