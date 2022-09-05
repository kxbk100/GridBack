#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Uos指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    """
    WC=(HIGH+LOW+2*CLOSE)/4
    N1=20
    N2=40
    EMA1=EMA(WC,N1)
    EMA2=EMA(WC,N2)
    WC 也可以用来代替收盘价构造一些技术指标（不过相对比较少用
    到）。我们这里用 WC 的短期均线和长期均线的交叉来产生交易信号。
    """
    WC = (df['high'] + df['low'] + 2 * df['close']) / 4  # WC=(HIGH+LOW+2*CLOSE)/4
    df['ema1'] = WC.ewm(n, adjust=False).mean()  # EMA1=EMA(WC,N1)
    df['ema2'] = WC.ewm(2 * n, adjust=False).mean()  # EMA2=EMA(WC,N2)
    # 去量纲
    df[factor_name] = df['ema1'] / (df['ema2'] + eps) - 1

    # 删除多余列
    del df['ema1'], df['ema2']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
