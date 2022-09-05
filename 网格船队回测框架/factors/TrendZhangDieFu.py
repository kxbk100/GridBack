#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # TrendZhangDieFu
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['涨跌幅'] = df['close'].pct_change(n).shift(1)
    high = df['high'].rolling(n, min_periods=1).max()
    low = df['low'].rolling(n, min_periods=1).min()
    df['振幅'] = (high / low - 1).shift(1)

    # 涨跌幅 / 振幅  的计算结果在[-1,1]之间，越大说明也趋近于单边上涨，越小说明越趋近于单边下跌
    df['单边趋势'] = df['涨跌幅'] / (df['振幅'] + eps)
    df[factor_name] = df['涨跌幅'] * abs(df['单边趋势'])

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
