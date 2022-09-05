#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff, eps


def signal(*args):
    # Dema指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    """
    N=60
    EMA=EMA(CLOSE,N)
    DEMA=2*EMA-EMA(EMA,N)
    DEMA 结合了单重 EMA 和双重 EMA，在保证平滑性的同时减少滞后
    性。
    """
    ema = df['close'].ewm(n, adjust=False).mean()  # EMA=EMA(CLOSE,N)
    ema_ema = ema.ewm(n, adjust=False).mean()  # EMA(EMA,N)
    dema = 2 * ema - ema_ema  # DEMA=2*EMA-EMA(EMA,N)
    # dema 去量纲
    df[factor_name] = dema / (ema + eps) - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
