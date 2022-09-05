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

    # ARBR指标
    """
    AR=SUM((HIGH-OPEN),N)/SUM((OPEN-LOW),N)*100
    # BR=SUM((HIGH-REF(CLOSE,1)),N)/SUM((REF(CLOSE,1)-LOW),N)*100
    AR 衡量开盘价在最高价、最低价之间的位置；BR 衡量昨日收盘价在
    今日最高价、最低价之间的位置。AR 为人气指标，用来计算多空双
    方的力量对比。当 AR 值偏低（低于 50）时表示人气非常低迷，股价
    很低，若从 50 下方上穿 50，则说明股价未来可能要上升，低点买入。
    当 AR 值下穿 200 时卖出。
    """
    df['HO'] = df['high'] - df['open']
    df['OL'] = df['open'] - df['low']
    df[factor_name] = df['HO'].rolling(n).sum() / df['OL'].rolling(n).sum() * 100

    del df['HO']
    del df['OL']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df





