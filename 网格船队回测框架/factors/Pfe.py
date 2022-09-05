#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Pfe指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # 计算首尾价格的直线距离
    totle_y = df['close'] - df['close'].shift(n - 1)
    direct_distance = (totle_y ** 2 + (n - 1) ** 2) ** 0.5
    # 计算相邻价格间的距离
    each_y = df['close'].diff()
    each_distance = (each_y ** 2 + 1) ** 0.5
    actual_distance = each_distance.rolling(n - 1).sum()
    # 计算PFE
    PFE = 100 * (direct_distance / actual_distance)
    pct_change = ((df['close'] - df['close'].shift(n - 1)) / df['close'].shift(n - 1))
    df[factor_name] = PFE * pct_change

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
