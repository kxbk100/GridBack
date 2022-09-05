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
    # ******************** TII ********************
    # N1=40
    # M=[N1/2]+1
    # N2=9
    # CLOSE_MA=MA(CLOSE,N1)
    # DEV=CLOSE-CLOSE_MA
    # DEVPOS=IF(DEV>0,DEV,0)
    # DEVNEG=IF(DEV<0,-DEV,0)
    # SUMPOS=SUM(DEVPOS,M)
    # SUMNEG=SUM(DEVNEG,M)
    # TII=100*SUMPOS/(SUMPOS+SUMNEG)
    # TII_SIGNAL=EMA(TII,N2)
    # TII的计算方式与RSI相同，只是把其中的前后两天价格变化替换为价格与均线的差值。
    # TII可以用来反映价格的趋势以及趋势的强度。一般认为TII>80(<20)时上涨（下跌）趋势强烈。
    # TII产生交易信号有几种不同的方法：上穿20买入，下穿80卖出（作为反转指标）；上穿50买入，下穿50卖出；
    # 上穿信号线买入，下穿信号线卖出。 如果TII上穿TII_SIGNAL，则产生买入信号； 如果TII下穿TII_SIGNAL，则产生卖出信号。
    close_ma = df['close'].rolling(n, min_periods=1).mean()
    dev = df['close'] - close_ma
    devpos = np.where(dev > 0, dev, 0)
    devneg = np.where(dev < 0, -dev, 0)
    sumpos = pd.Series(devpos).rolling(int(1 + n / 2), min_periods=1).sum()
    sumneg = pd.Series(devneg).rolling(int(1 + n / 2), min_periods=1).sum()

    tii = 100 * sumpos / (sumpos + sumneg)
    df[factor_name] = scale_01(tii, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
