#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    # IC 指标
    """
    N1=9
    N2=26
    N3=52
    TS=(MAX(HIGH,N1)+MIN(LOW,N1))/2
    KS=(MAX(HIGH,N2)+MIN(LOW,N2))/2
    SPAN_A=(TS+KS)/2
    SPAN_B=(MAX(HIGH,N3)+MIN(LOW,N3))/2
    在 IC 指标中，SPAN_A 与 SPAN_B 之间的部分称为云。如果价格在
    云上，则说明是上涨趋势（如果 SPAN_A>SPAN_B，则上涨趋势强
    烈；否则上涨趋势较弱）；如果价格在云下，则为下跌趋势（如果
    SPAN_A<SPAN_B，则下跌趋势强烈；否则下跌趋势较弱）。该指
    标的使用方式与移动平均线有许多相似之处，比如较快的线（TS）突
    破较慢的线（KS），价格突破 KS,价格突破云，SPAN_A 突破 SPAN_B
    等。我们产生信号的方式是：如果价格在云上方 SPAN_A>SPAN_B，
    则当价格上穿 KS 时买入；如果价格在云下方且 SPAN_A<SPAN_B，
    则当价格下穿 KS 时卖出。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    n2 = 3 * n
    n3 = 2 * n2
    df['max_high_1'] = df['high'].rolling(n, min_periods=1).max()
    df['min_low_1'] = df['low'].rolling(n, min_periods=1).min()
    df['TS'] = (df['max_high_1'] + df['min_low_1']) / 2
    df['max_high_2'] = df['high'].rolling(n2, min_periods=1).max()
    df['min_low_2'] = df['low'].rolling(n2, min_periods=1).min()
    df['KS'] = (df['max_high_2'] + df['min_low_2']) / 2
    df['span_A'] = (df['TS'] + df['KS']) / 2
    df['max_high_3'] = df['high'].rolling(n3, min_periods=1).max()
    df['min_low_3'] = df['low'].rolling(n3, min_periods=1).min()
    df['span_B'] = (df['max_high_3'] + df['min_low_3']) / 2

    # 去量纲
    df[factor_name] = df['span_A'] / df['span_B']

    del df['max_high_1']
    del df['max_high_2']
    del df['max_high_3']
    del df['min_low_1']
    del df['min_low_2']
    del df['min_low_3']
    del df['TS']
    del df['KS']
    del df['span_A']
    del df['span_B']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
