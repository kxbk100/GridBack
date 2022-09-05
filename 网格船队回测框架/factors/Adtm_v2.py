#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps

# =====函数  01归一化
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # Adtm 指标
    """
    N=20
    DTM=IF(OPEN>REF(OPEN,1),MAX(HIGH-OPEN,OPEN-REF(OP
    EN,1)),0)
    DBM=IF(OPEN<REF(OPEN,1),MAX(OPEN-LOW,REF(OPEN,1)-O
    PEN),0)
    STM=SUM(DTM,N)
    SBM=SUM(DBM,N)
    Adtm=(STM-SBM)/MAX(STM,SBM)
    Adtm 通过比较开盘价往上涨的幅度和往下跌的幅度来衡量市场的
    人气。Adtm 的值在-1 到 1 之间。当 Adtm 上穿 0.5 时，说明市场
    人气较旺；当 Adtm 下穿-0.5 时，说明市场人气较低迷。我们据此构
    造交易信号。
    当 Adtm 上穿 0.5 时产生买入信号；
    当 Adtm 下穿-0.5 时产生卖出信号。

    """
    tmp1_s = df['high'] - df['open']  # HIGH-OPEN
    tmp2_s = df['open'] - df['open'].shift(1)  # OPEN-REF(OPEN,1)
    tmp3_s = df['open'] - df['low']  # OPEN-LOW
    tmp4_s = df['open'].shift(1) - df['open']  # REF(OPEN,1)-OPEN

    dtm = np.where(df['open'] > df['open'].shift(1), np.maximum(tmp1_s, tmp2_s), 0)
    dbm = np.where(df['open'] < df['open'].shift(1), np.maximum(tmp3_s, tmp4_s), 0)
    stm = pd.Series(dtm).rolling(n, min_periods=1).sum()
    sbm = pd.Series(dbm).rolling(n, min_periods=1).sum()

    signal = (stm - sbm) / (1e-9 + pd.Series(stm).combine(pd.Series(sbm), max).values)
    df[factor_name] = scale_01(signal, n)



    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

    


    
