#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # MICD 指标
    """
    N=20
    N1=10
    N2=20
    M=10
    MI=CLOSE-REF(CLOSE,1)
    MTMMA=SMA(MI,N,1)
    DIF=MA(REF(MTMMA,1),N1)-MA(REF(MTMMA,1),N2)
    MICD=SMA(DIF,M,1)
    如果 MICD 上穿 0，则产生买入信号；
    如果 MICD 下穿 0，则产生卖出信号。
    """
    df['MI'] = df['close'] - df['close'].shift(1)
    df['MIMMA'] = df['MI'].rolling(n, min_periods=1).mean()
    df['MIMMA_MA1'] = df['MIMMA'].shift(1).rolling(n, min_periods=1).mean()
    df['MIMMA_MA2'] = df['MIMMA'].shift(1).rolling(2 *n, min_periods=1).mean()
    df['DIF'] = df['MIMMA_MA1'] - df['MIMMA_MA2']
    df['MICD'] = df['DIF'].rolling(n, min_periods=1).mean()
    # 去量纲
    df[factor_name] = df['DIF'] / df['MICD']

    del df['MI']
    del df['MIMMA']
    del df['MIMMA_MA1']
    del df['MIMMA_MA2']
    del df['DIF']
    del df['MICD']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df




