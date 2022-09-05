#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff, eps


def signal(*args):

    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # ADTM 指标
    """
    N=20
    DTM=IF(OPEN>REF(OPEN,1),MAX(HIGH-OPEN,OPEN-REF(OP
    EN,1)),0)
    DBM=IF(OPEN<REF(OPEN,1),MAX(OPEN-LOW,REF(OPEN,1)-O
    PEN),0)
    STM=SUM(DTM,N)
    SBM=SUM(DBM,N)
    ADTM=(STM-SBM)/MAX(STM,SBM)
    ADTM 通过比较开盘价往上涨的幅度和往下跌的幅度来衡量市场的
    人气。ADTM 的值在-1 到 1 之间。当 ADTM 上穿 0.5 时，说明市场
    人气较旺；当 ADTM 下穿-0.5 时，说明市场人气较低迷。我们据此构
    造交易信号。
    当 ADTM 上穿 0.5 时产生买入信号；
    当 ADTM 下穿-0.5 时产生卖出信号。

    """
    df['h_o'] = df['high'] - df['open']
    df['diff_open'] = df['open'] - df['open'].shift(1)
    max_value1 = df[['h_o', 'diff_open']].max(axis=1)
    df.loc[df['open'] > df['open'].shift(1), 'DTM'] = max_value1
    df['DTM'].fillna(value=0, inplace=True)

    df['o_l'] = df['open'] - df['low']
    max_value2 = df[['o_l', 'diff_open']].max(axis=1)
    # DBM = pd.where(df['open'] < df['open'].shift(1), max_value2, 0)
    df.loc[df['open'] < df['open'].shift(1), 'DBM'] = max_value2
    df['DBM'].fillna(value=0, inplace=True)

    df['STM'] = df['DTM'].rolling(n).sum()
    df['SBM'] = df['DBM'].rolling(n).sum()
    max_value3 = df[['STM', 'SBM']].max(axis=1)
    df[factor_name] = (df['STM'] - df['SBM']) / max_value3

    del df['h_o']
    del df['diff_open']
    del df['o_l']
    del df['STM']
    del df['SBM']
    del df['DBM']
    del df['DTM']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

