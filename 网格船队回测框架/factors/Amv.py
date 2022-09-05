#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):

    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # AMV 指标
    """
    N1=13
    N2=34
    AMOV=VOLUME*(OPEN+CLOSE)/2
    AMV1=SUM(AMOV,N1)/SUM(VOLUME,N1)
    AMV2=SUM(AMOV,N2)/SUM(VOLUME,N2)
    AMV 指标用成交量作为权重对开盘价和收盘价的均值进行加权移动
    平均。成交量越大的价格对移动平均结果的影响越大，AMV 指标减
    小了成交量小的价格波动的影响。当短期 AMV 线上穿/下穿长期 AMV
    线时，产生买入/卖出信号。
    """
    df['AMOV'] = df['volume'] * (df['open'] + df['close']) / 2
    df['AMV1'] = df['AMOV'].rolling(n).sum() / df['volume'].rolling(n).sum()
    # df['AMV2'] = df['AMOV'].rolling(n * 3).sum() / df['volume'].rolling(n * 3).sum()
    # 去量纲
    df[factor_name] = (df['AMV1'] - df['AMV1'].rolling(n).min()) / (df['AMV1'].rolling(n).max() - df['AMV1'].rolling(n).min()) # 标准化
    
    del df['AMOV']
    del df['AMV1']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df