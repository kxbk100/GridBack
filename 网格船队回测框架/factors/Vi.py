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
    # Vi 指标
    """
    TR=MAX([ABS(HIGH-LOW),ABS(LOW-REF(CLOSE,1)),ABS(HIG
    H-REF(CLOSE,1))])
    VMPOS=ABS(HIGH-REF(LOW,1))
    VMNEG=ABS(LOW-REF(HIGH,1))
    N=40
    SUMPOS=SUM(VMPOS,N)
    SUMNEG=SUM(VMNEG,N)
    TRSUM=SUM(TR,N)
    Vi+=SUMPOS/TRSUM
    Vi-=SUMNEG/TRSUM
    Vi 指标可看成 ADX 指标的变形。Vi 指标中的 Vi+与 Vi-与 ADX 中的
    DI+与 DI-类似。不同的是 ADX 中用当前高价与前一天高价的差和当
    前低价与前一天低价的差来衡量价格变化，而 Vi 指标用当前当前高
    价与前一天低价和当前低价与前一天高价的差来衡量价格变化。当
    Vi+上穿/下穿 Vi-时，多/空的信号更强，产生买入/卖出信号。
    """
    df['c1'] = abs(df['high'] - df['low'])
    df['c2'] = abs(df['close'] - df['close'].shift(1))
    df['c3'] = abs(df['high'] - df['close'].shift(1))
    df['TR'] = df[['c1', 'c2', 'c3']].max(axis=1)

    df['VMPOS'] = abs(df['high'] - df['low'].shift(1))
    df['VMNEG'] = abs(df['low'] - df['high'].shift(1))
    df['sum_pos'] = df['VMPOS'].rolling(n).sum()
    df['sum_neg'] = df['VMNEG'].rolling(n).sum()

    df['sum_tr'] = df['TR'].rolling(n).sum()
    df['Vi+'] = df['sum_pos'] / df['sum_tr']
    df['Vi-'] = df['sum_neg'] / df['sum_tr']
    df[factor_name] = df['Vi+'] - df['Vi-']
    # df[f'Vi+_bh_{n}'] = df['Vi+'].shift(1)
    # df[f'Vi-_bh_{n}'] = df['Vi-'].shift(1)
    # df[f'Vi_bh_{n}'] = df['Vi'].shift(1)

    del df['c1']
    del df['c2']
    del df['c3']
    del df['TR']
    del df['VMPOS']
    del df['VMNEG']
    del df['sum_pos']
    del df['sum_neg']
    del df['sum_tr']
    del df['Vi+']
    del df['Vi-']
    # del df['Vi']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df






