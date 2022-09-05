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

    # ADOSC 指标
    """
    AD=CUM_SUM(((CLOSE-LOW)-(HIGH-CLOSE))*VOLUME/(HIGH-LOW))
    AD_EMA1=EMA(AD,N1)
    AD_EMA2=EMA(AD,N2) 
    ADOSC=AD_EMA1-AD_EMA2
    ADL（收集派发线）指标是成交量的加权累计求和，其中权重为 CLV
    指标。ADL 指标可以与 OBV 指标进行类比。不同的是 OBV 指标只
    根据价格的变化方向把成交量分为正、负成交量再累加，而 ADL 是 用 CLV 指标作为权重进行成交量的累加。我们知道，CLV 指标衡量
    收盘价在最低价和最高价之间的位置，CLV>0(<0),则收盘价更靠近最
    高（低）价。CLV 越靠近 1(-1)，则收盘价越靠近最高（低）价。如
    果当天的 CLV>0，则 ADL 会加上成交量*CLV（收集）；如果当天的
    CLV<0，则 ADL 会减去成交量*CLV（派发）。
    ADOSC 指标是 ADL（收集派发线）指标的短期移动平均与长期移动
    平均之差。如果 ADOSC 上穿 0，则产生买入信号；如果 ADOSC 下 穿 0，则产生卖出信号。
    """
    df['AD'] = ((df['close'] - df['low']) - (df['high'] - df['close'])) * df['volume'] / (df['high'] - df['low'])
    df['AD_sum'] = df['AD'].cumsum()
    df['AD_EMA1'] = df['AD_sum'].ewm(n, adjust=False).mean()
    df['AD_EMA2'] = df['AD_sum'].ewm(n * 2, adjust=False).mean()
    df['ADOSC'] = df['AD_EMA1'] - df['AD_EMA2']

    # 标准化
    df[factor_name] = (df['ADOSC'] - df['ADOSC'].rolling(n).min()) / (df['ADOSC'].rolling(n).max() - df['ADOSC'].rolling(n).min())

    del df['AD']
    del df['AD_sum']
    del df['AD_EMA2']
    del df['AD_EMA1']
    del df['ADOSC']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
