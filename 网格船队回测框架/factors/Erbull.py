#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff

eps = 1e-8


def signal(*args):
    """
    N=20
    BullPower=HIGH-EMA(CLOSE,N)
    BearPower=LOW-EMA(CLOSE,N)
    ER 为动量指标。用来衡量市场的多空力量对比。在多头市场，人们
    会更贪婪地在接近高价的地方买入，BullPower 越高则当前多头力量
    越强；而在空头市场，人们可能因为恐惧而在接近低价的地方卖出。
    BearPower 越低则当前空头力量越强。当两者都大于 0 时，反映当前
    多头力量占据主导地位；两者都小于0则反映空头力量占据主导地位。
    如果 BearPower 上穿 0，则产生买入信号；
    如果 BullPower 下穿 0，则产生卖出信号。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    ema = df['close'].ewm(n, adjust=False).mean()  # EMA(CLOSE,N)
    bull_power = df['high'] - ema  # 越高表示上涨 牛市 BullPower=HIGH-EMA(CLOSE,N)
    bear_power = df['low'] - ema  # 越低表示下降越厉害  熊市 BearPower=LOW-EMA(CLOSE,N)
    df[factor_name] = bull_power / (ema + eps)  # 去量纲

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
