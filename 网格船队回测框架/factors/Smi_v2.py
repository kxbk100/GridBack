#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import talib
import pandas as pd
from utils.diff import add_diff

# =====函数  01归一化
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
        1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)

def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # ******************** smi ********************
    # --- SMI --- 073/125
    # N1=20
    # N2=20
    # N3=20
    # M=(Smi_v2X(HIGH,N1)+MIN(LOW,N1))/2
    # D=CLOSE-M
    # DS=ESmi_v2(ESmi_v2(D,N2),N2)
    # DHL=ESmi_v2(ESmi_v2(Smi_v2X(HIGH,N1)-MIN(LOW,N1),N2),N2)
    # SMI=100*DS/DHL
    # SMISmi_v2=Smi_v2(SMI,N3)
    # SMI指标可以看作KDJ指标的变形。不同的是，KD指标衡量的是当天收盘价位于最近N天的最高价和最低价之间的位置，
    # 而SMI指标是衡量当天收盘价与最近N天的最高价与最低价均值之间的距离。
    # 我们用SMI指标上穿/下穿其均线产生买入/卖出信号。

    m = 0.5 * df['high'].rolling(n, min_periods=1).max() + 0.5 * df['low'].rolling(n, min_periods=1).min()
    d = df['close'] - m
    ds = d.ewm(span=n, adjust=False, min_periods=1).mean()
    ds = ds.ewm(span=n, adjust=False, min_periods=1).mean()

    dhl = df['high'].rolling(n, min_periods=1).max() - df['low'].rolling(n, min_periods=1).min()
    dhl = dhl.ewm(span=n, adjust=False, min_periods=1).mean()
    dhl = dhl.ewm(span=n, adjust=False, min_periods=1).mean()

    smi = 100 * ds / dhl

    signal = smi.rolling(n, min_periods=1).mean()
    df[factor_name] = scale_01(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
