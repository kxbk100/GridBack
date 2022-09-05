#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # Rwi 指标
    """
    N=14
    TR=MAX(ABS(HIGH-LOW),ABS(HIGH-REF(CLOSE,1)),ABS(REF(
    CLOSE,1)-LOW))
    ATR=MA(TR,N)
    RwiH=(HIGH-REF(LOW,1))/(ATR*√N)
    RwiL=(REF(HIGH,1)-LOW)/(ATR*√N)
    Rwi（随机漫步指标）对一段时间股票的随机漫步区间与真实运动区
    间进行比较以判断股票价格的走势。
    如果 RwiH>1，说明股价长期是上涨趋势，则产生买入信号；
    如果 RwiL>1，说明股价长期是下跌趋势，则产生卖出信号。
    """
    df['c1'] = abs(df['high'] - df['low'])
    df['c2'] = abs(df['close'] - df['close'].shift(1))
    df['c3'] = abs(df['high'] - df['close'].shift(1))
    df['TR'] = df[['c1', 'c2', 'c3']].max(axis=1)
    df['ATR'] = df['TR'].rolling(n, min_periods=1).mean()
    df[factor_name] = (df['high'] - df['low'].shift(1)) / (df['ATR'] * np.sqrt(n))
    # df['RwiL'] = (df['high'].shift(1) - df['low']) / (df['ATR'] * np.sqrt(n))
    # df['Rwi'] = (df['close'] - df['RwiL']) / (1e-9 + df['RwiH'] - df['RwiL'])
    # df[f'RwiH_bh_{n}'] = df['RwiH'].shift(1)
    # df[f'RwiL_bh_{n}'] = df['RwiL'].shift(1)
    # df[f'Rwi_bh_{n}'] = df['Rwi'].shift(1)

    del df['c1']
    del df['c2']
    del df['c3']
    del df['TR']
    del df['ATR']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df



