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

    # BOP 指标
    """
    N=20
    BOP=MA((CLOSE-OPEN)/(HIGH-LOW),N)
    BOP 的变化范围为-1 到 1，用来衡量收盘价与开盘价的距离（正、负
    距离）占最高价与最低价的距离的比例，反映了市场的多空力量对比。
    如果 BOP>0，则多头更占优势；BOP<0 则说明空头更占优势。BOP
    越大，则说明价格被往最高价的方向推动得越多；BOP 越小，则说
    明价格被往最低价的方向推动得越多。我们可以用 BOP 上穿/下穿 0
    线来产生买入/卖出信号。
    """
    df['co'] = df['close'] - df['open']
    df['hl'] = df['high'] - df['low']
    df[factor_name] = (df['co'] / df['hl']).rolling(n, min_periods=1).mean()

    del df['co']
    del df['hl']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
