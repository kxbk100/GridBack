#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # Si 指标
    """
    A=ABS(HIGH-REF(CLOSE,1))
    B=ABS(LOW-REF(CLOSE,1))
    C=ABS(HIGH-REF(LOW,1))
    D=ABS(REF(CLOSE,1)-REF(OPEN,1))
    N=20
    K=MAX(A,B)
    M=MAX(HIGH-LOW,N)
    R1=A+0.5*B+0.25*D
    R2=B+0.5*A+0.25*D
    R3=C+0.25*D
    R4=IF((A>=B) & (A>=C),R1,R2)
    R=IF((C>=A) & (C>=B),R3,R4)
    Si=50*(CLOSE-REF(CLOSE,1)+(REF(CLOSE,1)-REF(OPEN,1))+
    0.5*(CLOSE-OPEN))/R*K/M
    Si 用价格变化（即两天收盘价之差，昨日收盘与开盘价之差，今日收
    盘与开盘价之差）的加权平均来反映价格的变化。如果 Si 上穿/下穿
    0 则产生买入/卖出信号。
    """
    df['A'] = abs(df['high'] - df['close'].shift(1))
    df['B'] = abs(df['low'] - df['close'].shift(1))
    df['C'] = abs(df['high'] - df['low'].shift(1))
    df['D'] = abs(df['close'].shift(1) - df['open'].shift(1))
    df['K'] = df[['A', 'B']].max(axis=1)
    df['M'] = (df['high'] - df['low']).rolling(n).max()
    df['R1'] = df['A'] + 0.5 * df['B'] + 0.25 * df['D']
    df['R2'] = df['B'] + 0.5 * df['A'] + 0.25 * df['D']
    df['R3'] = df['C'] + 0.25 * df['D']
    df['R4'] = np.where((df['A'] >= df['B']) & (df['A'] >= df['C']), df['R1'], df['R2'])
    df['R'] = np.where((df['C'] >= df['A']) & (df['C'] >= df['B']), df['R3'], df['R4'])
    df[factor_name] = 50 * (df['close'] - df['close'].shift(1) + (df['close'].shift(1) - df['open'].shift(1)) +
                     0.5 * (df['close'] - df['open'])) / df['R'] * df['K'] / df['M']

    
    del df['A']
    del df['B']
    del df['C']
    del df['D']
    del df['K']
    del df['M']
    del df['R1']
    del df['R2']
    del df['R3']
    del df['R4']
    del df['R']
    # del df['Si']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df



