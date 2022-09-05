#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff,eps


def signal(*args):
    # Trix
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    df['ema'] = df['close'].ewm(n, adjust=False).mean()  # EMA(CLOSE,N)
    df['ema_ema'] = df['ema'].ewm(n, adjust=False).mean()  # EMA(EMA(CLOSE,N),N)
    df['ema_ema_ema'] = df['ema_ema'].ewm(n, adjust=False).mean()  # EMA(EMA(EMA(CLOSE,N),N),N)
    # TRIX=(TRIPLE_EMA-REF(TRIPLE_EMA,1))/REF(TRIPLE_EMA,1)
    df[factor_name] = (df['ema_ema_ema'] - df['ema_ema_ema'].shift(1)) / (df['ema_ema_ema'].shift(1) + eps)

    # 删除多余列
    del df['ema'], df['ema_ema'], df['ema_ema_ema']
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
