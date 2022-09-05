#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff


def signal(*args):
    #该指标使用时注意n不能大于过滤K线数量的一半（不是获取K线数据的一半）

    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['force'] = df['quote_volume'] * (df['close'] - df['close'].shift(1))
    df[factor_name] = df['force']/ df['force'].rolling(n, min_periods=1).mean()

    # ref = ma.shift(n)  # MADisplaced=REF(MA_CLOSE,M)


    del df['force']


    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
