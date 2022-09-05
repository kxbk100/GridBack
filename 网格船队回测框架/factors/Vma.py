#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff, eps


def signal(*args):
    # Vma
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    """
    N=20
    PRICE=(HIGH+LOW+OPEN+CLOSE)/4
    VMA=MA(PRICE,N)
    VMA 就是简单移动平均把收盘价替换为最高价、最低价、开盘价和
    收盘价的平均值。当 PRICE 上穿/下穿 VMA 时产生买入/卖出信号。
    """
    price = (df['high'] + df['low'] + df['open'] + df['close']) / 4  # PRICE=(HIGH+LOW+OPEN+CLOSE)/4
    vma = price.rolling(n, min_periods=1).mean()  # VMA=MA(PRICE,N)
    df[factor_name] = price / (vma + eps) - 1  # 去量纲

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

