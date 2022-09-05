#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # 计算魔改CCI指标
    open_ma = df['open'].rolling(n, min_periods=1).mean()
    high_ma = df['high'].rolling(n, min_periods=1).mean()
    low_ma = df['low'].rolling(n, min_periods=1).mean()
    close_ma = df['close'].rolling(n, min_periods=1).mean()
    tp = (high_ma + low_ma + close_ma) / 3
    ma = tp.rolling(n, min_periods=1).mean()
    md = abs(ma - close_ma).rolling(n, min_periods=1).mean()
    df[factor_name] = ((tp - ma) / md / 0.015)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
