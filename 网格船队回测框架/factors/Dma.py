#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Dma 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    atr = ta.ATR(df['high'], df['low'], df['close'], timeperiod=n)
    atr_x = atr / atr.rolling(n, min_periods=1).sum()

    ma_short = df['close'].rolling(n, min_periods=1).mean()
    ma_long = df['close'].rolling(2 * n, min_periods=1).mean()
    ma_dif = ma_short - ma_long
    dma = (ma_dif / abs(ma_dif).rolling(2 * n, min_periods=1).sum()) + 1
    df[factor_name] = dma * (1 + atr_x)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
