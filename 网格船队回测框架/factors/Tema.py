#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Tema指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    """
    N=20,40
    TEMA=3*EMA(CLOSE,N)-3*EMA(EMA(CLOSE,N),N)+EMA(EMA(EMA(CLOSE,N),N),N)
    TEMA 结合了单重、双重和三重的 EMA，相比于一般均线延迟性较
    低。我们用快、慢 TEMA 的交叉来产生交易信号。
    """
    df['ema'] = df['close'].ewm(n, adjust=False).mean()  # EMA(CLOSE,N)
    df['ema_ema'] = df['ema'].ewm(
        n, adjust=False).mean()  # EMA(EMA(CLOSE,N),N)
    df['ema_ema_ema'] = df['ema_ema'].ewm(
        n, adjust=False).mean()  # EMA(EMA(EMA(CLOSE,N),N),N)
    # TEMA=3*EMA(CLOSE,N)-3*EMA(EMA(CLOSE,N),N)+EMA(EMA(EMA(CLOSE,N),N),N)
    df['TEMA'] = 3 * df['ema'] - 3 * df['ema_ema'] + df['ema_ema_ema']
    # 去量纲
    df[factor_name] = df['ema'] / (df['TEMA'] + eps) - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
