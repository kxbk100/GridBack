#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff


def signal(*args):
    #该指标使用时注意n不能大于过滤K线数量的一半（不是获取K线数据的一半）
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['oma'] = df['open'].ewm(span=n, adjust=False).mean()
    df['hma'] = df['high'].ewm(span=n, adjust=False).mean()
    df['lma'] = df['low'].ewm(span=n, adjust=False).mean()
    df['cma'] = df['close'].ewm(span=n, adjust=False).mean()
    df['tp'] = (df['oma'] + df['hma'] + df['lma'] + df['cma']) / 4
    df['ma'] = df['tp'].ewm(span=n, adjust=False).mean()
    df['abs_diff_close'] = abs(df['tp'] - df['ma'])
    df['md'] = df['abs_diff_close'].ewm(span=n, adjust=False).mean()

    df[factor_name] = (df['tp'] - df['ma']) / df['md']

    # # 删除中间数据
    del df['oma']
    del df['hma']
    del df['lma']
    del df['cma']
    del df['tp']
    del df['ma']
    del df['abs_diff_close']
    del df['md']







    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
