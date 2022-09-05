#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    # DO 指标
    """
    DO=EMA(EMA(RSI,N),M)
    DO 是平滑处理（双重移动平均）后的 RSI 指标。DO 大于 0 则说明
    市场处于上涨趋势，小于 0 说明市场处于下跌趋势。我们用 DO 上穿
    /下穿其移动平均线来产生买入/卖出信号。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    diff = df['close'].diff()
    df['up'] = np.where(diff > 0, diff, 0)
    df['down'] = np.where(diff < 0, abs(diff), 0)
    A = df['up'].rolling(n).sum()
    B = df['down'].rolling(n).sum()
    df['rsi'] = A / (A + B)
    df['ema_rsi'] = df['rsi'].ewm(n, adjust=False).mean()
    df[factor_name] = df['ema_rsi'].ewm(n, adjust=False).mean()

    del df['up']
    del df['down']
    del df['rsi']
    del df['ema_rsi']
 
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
