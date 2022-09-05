#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):

    # OSC 指标
    """
    N=40
    M=20
    OSC=CLOSE-MA(CLOSE,N)
    OSCMA=MA(OSC,M)
    OSC 反映收盘价与收盘价移动平均相差的程度。如果 OSC 上穿/下 穿 OSCMA 则产生买入/卖出信号。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['ma'] = df['close'].rolling(2 * n, min_periods=1).mean()
    df['OSC'] = df['close'] - df['ma']
    df[factor_name] = df['OSC'].rolling(n, min_periods=1).mean()

    del df['ma']
    del df['OSC']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df