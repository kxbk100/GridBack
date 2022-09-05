#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # T3
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    va = 0.5
    ema = df['close'].ewm(n, adjust=False).mean()  # EMA(CLOSE,N)
    ema_ema = ema.ewm(n, adjust=False).mean()  # EMA(EMA(CLOSE,N),N)
    T1 = ema * (1 + va) - ema_ema * va
    T1_ema = T1.ewm(n, adjust=False).mean()  # EMA(T1,N)
    T1_ema_ema = T1_ema.ewm(n, adjust=False).mean()  # EMA(EMA(T1,N),N)
    T2 = T1_ema * (1 + va) - T1_ema_ema * va
    T2_ema = T2.ewm(n, adjust=False).mean()  # EMA(T2,N)
    T2_ema_ema = T2_ema.ewm(n, adjust=False).mean()  # EMA(EMA(T2,N),N)
    T3 = T2_ema * (1 + va) - T2_ema_ema * va
    df[factor_name] = df['close'] / (T3 + eps) - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
