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
    # CMF 指标
    """
    N=60
    CMF=SUM(((CLOSE-LOW)-(HIGH-CLOSE))*VOLUME/(HIGH-LOW),N)/SUM(VOLUME,N)
    CMF 用 CLV 对成交量进行加权，如果收盘价在高低价的中点之上，
    则为正的成交量（买方力量占优势）；若收盘价在高低价的中点之下，
    则为负的成交量（卖方力量占优势）。
    如果 CMF 上穿 0，则产生买入信号；
    如果 CMF 下穿 0，则产生卖出信号。
    """
    A = ((df['close'] - df['low']) - (df['high'] - df['close']) )* df['volume'] / (df['high'] - df['low'])
    df[factor_name] = A.rolling(n).sum() / df['volume'].rolling(n).sum()

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df