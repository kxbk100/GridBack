#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):

    # STC 指标
    """
    N1=23
    N2=50
    N=40
    MACDX=EMA(CLOSE,N1)-EMA(CLOSE,N2)
    V1=MIN(MACDX,N)
    V2=MAX(MACDX,N)-V1
    FK=IF(V2>0,(MACDX-V1)/V2*100,REF(FK,1))
    FD=SMA(FK,N,1)
    V3=MIN(FD,N)
    V4=MAX(FD,N)-V3
    SK=IF(V4>0,(FD-V3)/V4*100,REF(SK,1))
    STC=SD=SMA(SK,N,1) 
    STC 指标结合了 MACD 指标和 KDJ 指标的算法。首先用短期均线与
    长期均线之差算出 MACD，再求 MACD 的随机快速随机指标 FK 和
    FD，最后求 MACD 的慢速随机指标 SK 和 SD。其中慢速随机指标就
    是 STC 指标。STC 指标可以用来反映市场的超买超卖状态。一般认
    为 STC 指标超过 75 为超买，STC 指标低于 25 为超卖。
    如果 STC 上穿 25，则产生买入信号；
    如果 STC 下穿 75，则产生卖出信号。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    N1 = n
    N2 = int(N1 * 1.5) # 大约值
    N = 2 * n
    df['ema1'] = df['close'].ewm(N1, adjust=False).mean()
    df['ema2'] = df['close'].ewm(N, adjust=False).mean()
    df['MACDX'] = df['ema1'] - df['ema2']
    df['V1'] = df['MACDX'].rolling(N2, min_periods=1).min()
    df['V2'] = df['MACDX'].rolling(N2, min_periods=1).max()- df['V1']
    df['FK'] = (df['MACDX'] - df['V1']) / df['V2'] * 100
    df['FK'] = np.where(df['V2'] > 0, (df['MACDX'] - df['V1']) / df['V2'] * 100, df['FK'].shift(1))
    df['FD'] = df['FK'].rolling(N2, min_periods=1).mean()
    df['V3'] = df['FD'].rolling(N2, min_periods=1).min()
    df['V4'] = df['FD'].rolling(N2, min_periods=1).max() - df['V3']
    df['SK'] = (df['FD'] - df['V3']) / df['V4'] * 100
    df['SK'] = np.where(df['V4'] > 0, (df['FD'] - df['V3']) / df['V4'] * 100, df['SK'].shift(1))
    df[factor_name] = df['SK'].rolling(N1, min_periods=1).mean()

    del df['ema1']
    del df['ema2']
    del df['MACDX']
    del df['V1']
    del df['V2']
    del df['V3']
    del df['V4']
    del df['FK']
    del df['FD']
    del df['SK']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df










        