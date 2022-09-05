#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff


def signal(*args):
    #该指标使用时注意n不能大于过滤K线数量的一半（不是获取K线数据的一半）
    """
    N=20
    M=10
    MA_CLOSE=MA(CLOSE,N)
    MADisplaced=REF(MA_CLOSE,M)
    MADisplaced 指标把简单移动平均线向前移动了 M 个交易日，用法
    与一般的移动平均线一样。如果收盘价上穿/下穿 MADisplaced 则产
    生买入/卖出信号。
    有点变种bias
    """
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    ma = df['close'].rolling(
        2 * n, min_periods=1).mean()  # MA(CLOSE,N) 固定俩个参数之间的关系  减少参数
    ref = ma.shift(n)  # MADisplaced=REF(MA_CLOSE,M)

    df[factor_name] = df['close'] / ref - 1  # 去量纲



    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
