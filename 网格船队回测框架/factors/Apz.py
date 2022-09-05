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
    """
    N=10
    M=20
    PARAM=2
    VOL=EMA(EMA(HIGH-LOW,N),N)
    UPPER=EMA(EMA(CLOSE,M),M)+PARAM*VOL
    LOWER= EMA(EMA(CLOSE,M),M)-PARAM*VOL
    APZ（Adaptive Price Zone 自适应性价格区间）与布林线 Bollinger 
    Band 和肯通纳通道 Keltner Channel 很相似，都是根据价格波动性围
    绕均线而制成的价格通道。只是在这三个指标中计算价格波动性的方
    法不同。在布林线中用了收盘价的标准差，在肯通纳通道中用了真波
    幅 ATR，而在 APZ 中运用了最高价与最低价差值的 N 日双重指数平
    均来反映价格的波动幅度。
    """
    df['hl'] = df['high'] - df['low']
    df['ema_hl'] = df['hl'].ewm(n, adjust=False).mean()
    df['vol'] = df['ema_hl'].ewm(n, adjust=False).mean()

    # 计算通道 可以作为CTA策略 作为因子的时候进行改造
    df['ema_close'] = df['close'].ewm(2 * n, adjust=False).mean()
    df['ema_ema_close'] = df['ema_close'].ewm(2 * n, adjust=False).mean()
    # EMA去量纲
    df[factor_name] = df['vol'] / df['ema_ema_close']

    del df['hl']
    del df['ema_hl']
    del df['vol']
    del df['ema_close']
    del df['ema_ema_close']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df





    