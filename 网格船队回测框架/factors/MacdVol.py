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
    # MACDVOL 指标
    """
    N1=20
    N2=40
    N3=10
    MACDVOL=EMA(VOLUME,N1)-EMA(VOLUME,N2)
    SIGNAL=MA(MACDVOL,N3)
    MACDVOL 是 MACD 的成交量版本。如果 MACDVOL 上穿 SIGNAL，
    则买入；下穿 SIGNAL 则卖出。
    """
    N1 = 2 * n
    N2 = 4 * n
    N3 = n
    df['ema_volume_1'] = df['volume'].ewm(N1, adjust=False).mean()
    df['ema_volume_2'] = df['volume'].ewm(N2, adjust=False).mean()
    df['MACDV'] = df['ema_volume_1'] - df['ema_volume_2']
    df['SIGNAL'] = df['MACDV'].rolling(N3, min_periods=1).mean()
    # 去量纲
    df[factor_name] = df['MACDV'] / df['SIGNAL'] - 1
    
    del df['ema_volume_1']
    del df['ema_volume_2']
    del df['MACDV']
    del df['SIGNAL']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df