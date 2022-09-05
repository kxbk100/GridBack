#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):

    # WVAD 指标
    """
    N=20
    WVAD=SUM(((CLOSE-OPEN)/(HIGH-LOW)*VOLUME),N)
    WVAD 是用价格信息对成交量加权的价量指标，用来比较开盘到收盘
    期间多空双方的力量。WVAD 的构造与 CMF 类似，但是 CMF 的权
    值用的是 CLV(反映收盘价在最高价、最低价之间的位置)，而 WVAD
    用的是收盘价与开盘价的距离（即蜡烛图的实体部分的长度）占最高
    价与最低价的距离的比例，且没有再除以成交量之和。
    WVAD 上穿 0 线，代表买方力量强；
    WVAD 下穿 0 线，代表卖方力量强。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['VAD'] = (df['close'] - df['open']) / (df['high'] - df['low']) * df['volume']
    df['WVAD'] = df['VAD'].rolling(n).sum()

    # 标准化
    df[factor_name] = (df['WVAD'] - df['WVAD'].rolling(n).min()) / (df['WVAD'].rolling(n).max() - df['WVAD'].rolling(n).min())

    del df['VAD']
    del df['WVAD']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
