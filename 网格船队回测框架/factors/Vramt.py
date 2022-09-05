#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff, eps

eps = 1e-8


def signal(*args):
    """
    N=40
    AV=IF(CLOSE>REF(CLOSE,1),AMOUNT,0)
    BV=IF(CLOSE<REF(CLOSE,1),AMOUNT,0)
    CV=IF(CLOSE=REF(CLOSE,1),AMOUNT,0)
    AVS=SUM(AV,N)
    BVS=SUM(BV,N)
    CVS=SUM(CV,N)
    VRAMT=(AVS+CVS/2)/(BVS+CVS/2)
    VRAMT 的计算与 VR 指标（Volume Ratio）一样，只是把其中的成
    交量替换成了成交额。
    如果 VRAMT 上穿 180，则产生买入信号；
    如果 VRAMT 下穿 70，则产生卖出信号。
    """

    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['AV'] = np.where(df['close'] > df['close'].shift(1), df['volume'], 0)  # AV=IF(CLOSE>REF(CLOSE,1),AMOUNT,0)
    df['BV'] = np.where(df['close'] < df['close'].shift(1), df['volume'], 0)  # BV=IF(CLOSE<REF(CLOSE,1),AMOUNT,0)
    df['CV'] = np.where(df['close'] == df['close'].shift(1), df['volume'], 0)  # CV=IF(CLOSE=REF(CLOSE,1),AMOUNT,0)
    df['AVS'] = df['AV'].rolling(n, min_periods=1).sum()  # AVS=SUM(AV,N)
    df['BVS'] = df['BV'].rolling(n, min_periods=1).sum()  # BVS=SUM(BV,N)
    df['CVS'] = df['CV'].rolling(n, min_periods=1).sum()  # CVS=SUM(CV,N)
    df[factor_name] = (df['AVS'] + df['CVS'] / 2) / (df['BVS'] + df['CVS'] / 2 + eps)  # VRAMT=(AVS+CVS/2)/(BVS+CVS/2)

    del df['AV']
    del df['BV']
    del df['CV']
    del df['AVS']
    del df['BVS']
    del df['CVS']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
