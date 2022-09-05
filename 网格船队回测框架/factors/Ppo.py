#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    # PPo 指标
    
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    N3 = n
    N1 = int(n * 1.382)
    N2 = 3 * n
    df['ema_1'] = df['close'].ewm(
        N1, adjust=False).mean()  # EMA(CLOSE,N1)
    df['ema_2'] = df['close'].ewm(
        N2, adjust=False).mean()  # EMA(CLOSE,N2)
    # PPO=(EMA(CLOSE,N1)-EMA(CLOSE,N2))/EMA(CLOSE,N2)
    df['PPO'] = (df['ema_1'] - df['ema_2']) / df['ema_2']
    df[factor_name] = df['PPO'].ewm(N3, adjust=False).mean()  # PPO_SIGNAL=EMA(PPO,N3)

    del df['ema_1']
    del df['ema_2']
    del df['PPO']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df










        
