#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff

def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)

def signal(*args):
    df = args[0]
    n  = args[1]    
    diff_num = args[2]
    factor_name = args[3]
# ApzLower 指标
    """
    N=10
    M=20
    PARAM=2
    VOL=EMA(EMA(HIGH-LOW,N),N)
    UPPER=EMA(EMA(CLOSE,M),M)+PARAM*VOL
    LOWER= EMA(EMA(CLOSE,M),M)-PARAM*VOL
    ApzLower（Adaptive Price Zone 自适应性价格区间）与布林线 Bollinger 
    Band 和肯通纳通道 Keltner Channel 很相似，都是根据价格波动性围
    绕均线而制成的价格通道。只是在这三个指标中计算价格波动性的方
    法不同。在布林线中用了收盘价的标准差，在肯通纳通道中用了真波
    幅 ATR，而在 ApzLower 中运用了最高价与最低价差值的 N 日双重指数平
    均来反映价格的波动幅度。
    """
    vol = (df['high'] - df['low']).ewm(span=n, adjust=False, min_periods=1).mean().ewm(
        span=n, adjust=False, min_periods=1).mean()
    upper = df['close'].ewm(span=int(2 * n), adjust=False, min_periods=1).mean().ewm(
        span=int(2 * n), adjust=False, min_periods=1).mean() + 2 * vol

    signal = upper - 4 * vol
    df[factor_name] = scale_01(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df




    
