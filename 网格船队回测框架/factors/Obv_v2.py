#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    # 该指标使用时注意n不能大于过滤K线数量的一半（不是获取K线数据的一半）

    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['_va'] = (df['close'] - df['low'] - (df['high'] - df['close'])) / (df['high'] - df['low']) * df['volume']
    df['_obv'] = df['_va'].rolling(n).sum()

    # ref = ma.shift(n)  # MADisplaced=REF(MA_CLOSE,M)

    df[factor_name] = df['_obv'] / df['_obv'].rolling(n).mean()  # 去量纲


    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
