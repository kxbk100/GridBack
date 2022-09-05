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
    # ******************** TDI ********************
    # RSI_PriceLine=EMA(RSI,N2)
    # RSI_SignalLine=EMA(RSI,N3)
    # RSI_MarketLine=EMA(RSI,N4)
    # DI是根据RSI指标构造得到的技术指标，包括RSI价格线，交易信号线，市场基线等。
    # RSI价格线同时上穿/下穿交易信号线、市场基线时产生买入/卖出信号。

    rtn = df['close'].diff()
    up = np.where(rtn > 0, rtn, 0)
    dn = np.where(rtn < 0, rtn.abs(), 0)
    a = pd.Series(up).rolling(n, min_periods=1).sum()
    b = pd.Series(dn).rolling(n, min_periods=1).sum()
    a *= 1e3
    b *= 1e3
    rsi = a / (1e-9 + a + b)
    rsi_price_line = pd.Series(rsi).ewm(span=n, adjust=False, min_periods=1).mean()
    rsi_signal_line = pd.Series(rsi).ewm(span=int(2 * n), adjust=False, min_periods=1).mean()

    signal = rsi_price_line - rsi_signal_line
    df[factor_name] = scale_01(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
