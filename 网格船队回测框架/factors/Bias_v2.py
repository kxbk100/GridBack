#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Bias_v2
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # 计算线性回归
    df['new_close'] = ta.LINEARREG(df['close'], timeperiod=n)
    # EMA再次平滑曲线
    df['new_close'] = ta.EMA(df['new_close'], timeperiod=n)
    # 以新的收盘价计算中轨
    ma = df['new_close'].rolling(n, min_periods=1).mean()
    # 修改收盘价的定义为 最高和最低价的平均值 * 成交量
    df['_close'] = (df['high'] + df['low']) / 2 * df['volume']
    # 计算bias
    df[factor_name] = df['_close'] / (ma + eps) - 1

    del df['new_close'], df['_close']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
