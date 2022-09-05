#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff


def signal(*args):
    # RCCD 指标
    """
    M=40
    N1=20
    N2=40
    RC=CLOSE/REF(CLOSE,M)
    ARC1=SMA(REF(RC,1),M,1)
    DIF=MA(REF(ARC1,1),N1)-MA(REF(ARC1,1),N2)
    RCCD=SMA(DIF,M,1)
    RC 指标为当前价格与昨日价格的比值。当 RC 指标>1 时，说明价格在上升；当 RC 指标增大时，说明价格上升速度在增快。当 RC 指标
    <1 时，说明价格在下降；当 RC 指标减小时，说明价格下降速度在增
    快。RCCD 指标先对 RC 指标进行平滑处理，再取不同时间长度的移
    动平均的差值，再取移动平均。如 RCCD 上穿/下穿 0 则产生买入/
    卖出信号。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['RC'] = df['close'] / df['close'].shift(2 * n)
    df['ARC1'] = df['RC'].rolling(2 * n, min_periods=1).mean()
    df['MA1'] = df['ARC1'].shift(1).rolling(n, min_periods=1).mean()
    df['MA2'] = df['ARC1'].shift(1).rolling(2 * n, min_periods=1).mean()
    df['DIF'] = df['MA1'] - df['MA2']
    df[factor_name] = df['DIF'].rolling(2 * n, min_periods=1).mean()

    del df['RC']
    del df['ARC1']
    del df['MA1']
    del df['MA2']
    del df['DIF']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
