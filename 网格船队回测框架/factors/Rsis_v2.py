#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import talib
import pandas as pd
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # RSIS 指标
    """
    N=120
    M=20
    CLOSE_DIFF_POS=IF(CLOSE>REF(CLOSE,1),CLOSE-REF(CL
    OSE,1),0)
    RSI=SMA(CLOSE_DIFF_POS,N,1)/SMA(ABS(CLOSE-REF(CLOS
    E,1)),N,1)*100
    RSIS=(RSI-MIN(RSI,N))/(MAX(RSI,N)-MIN(RSI,N))*100
    RSISMA=EMA(RSIS,M)
    RSIS 反映当前 RSI 在最近 N 天的 RSI 最大值和最小值之间的位置，
    与 KDJ 指标的构造思想类似。由于 RSIS 波动性比较大，我们先取移
    动平均再用其产生信号。其用法与 RSI 指标的用法类似。
    RSISMA 上穿 40 则产生买入信号；
    RSISMA 下穿 60 则产生卖出信号。
    """
    close_diff_pos = np.where(df['close'] > df['close'].shift(1), df['close'] - df['close'].shift(1), 0)
    rsi_a = pd.Series(close_diff_pos).ewm(alpha=1/(4*n), adjust=False).mean()
    rsi_b = (df['close'] - df['close'].shift(1)).abs().ewm(alpha=1/(4*n), adjust=False).mean()
    rsi = 100 * rsi_a / (1e-9 + rsi_b)
    rsi_min = pd.Series(rsi).rolling(int(4*n), min_periods=1).min()
    rsi_max = pd.Series(rsi).rolling(int(4 * n), min_periods=1).max()
    df[factor_name] = 100 * (rsi - rsi_min) / (1e-9 + rsi_max - rsi_min)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df









        
