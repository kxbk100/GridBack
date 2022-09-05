#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
from utils.diff import add_diff, eps


def signal(*args):
    # Cv 指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    """
    N=10
    H_L_EMA=EMA(HIGH-LOW,N)
    CV=(H_L_EMA-REF(H_L_EMA,N))/REF(H_L_EMA,N)*100
    CV 指标用来衡量股价的波动，反映一段时间内最高价与最低价之差
    （价格变化幅度）的变化率。如果 CV 的绝对值下穿 30，买入；
    如果 CV 的绝对值上穿 70，卖出。
    """
    # H_L_EMA=EMA(HIGH-LOW,N)
    df['H_L_ema'] = (df['high'] - df['low']).ewm(n, adjust=False).mean()  
    df[factor_name] = (df['H_L_ema'] - df['H_L_ema'].shift(n)) / \
        (df['H_L_ema'].shift(n) + eps) * 100

    del df['H_L_ema']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
