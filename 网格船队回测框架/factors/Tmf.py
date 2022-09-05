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
    # TMF 指标
    """
    N=80
    HIGH_TRUE=MAX(HIGH,REF(CLOSE,1))
    LOW_TRUE=MIN(LOW,REF(CLOSE,1))
    TMF=EMA(VOL*(2*CLOSE-HIGH_TRUE-LOW_TRUE)/(HIGH_TR
    UE-LOW_TRUE),N)/EMA(VOL,N)
    TMF 指标和 CMF 指标类似，都是用价格对成交量加权。但是 CMF
    指标用 CLV 做权重，而 TMF 指标用的是真实最低价和真实最高价，
    且取的是移动平均而不是求和。如果 TMF 上穿 0，则产生买入信号；
    如果 TMF 下穿 0，则产生卖出信号。
    """
    df['ref'] = df['close'].shift(1)
    df['max_high'] = df[['high', 'ref']].max(axis=1)
    df['min_low'] = df[['low', 'ref']].min(axis=1)

    T = df['volume'] * ( 2 * df['close'] - df['max_high'] - df['min_low']) / (df['max_high'] - df['min_low'])
    df[factor_name] = T.ewm(n, adjust=False).mean() / df['volume'].ewm(n, adjust=False).mean()
    
    del df['ref']
    del df['max_high']
    del df['min_low']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df





