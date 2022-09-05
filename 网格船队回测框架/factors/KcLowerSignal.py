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
    # ******************** KC ********************
    # N=14
    # TR=MAX(ABS(HIGH-LOW),ABS(HIGH-REF(CLOSE,1)),ABS(REF(CLOSE,1)-REF(LOW,1)))
    # ATR=MA(TR,N)
    # Middle=EMA(CLOSE,20)
    # UPPER=MIDDLE+2*ATR
    # LOWER=MIDDLE-2*ATR
    # KC指标（KeltnerChannel）与布林带类似，都是用价格的移动平均构造中轨，不同的是表示波幅的方法，
    # 这里用ATR来作为波幅构造上下轨。价格突破上轨，可看成新的上升趋势，买入；价格突破下轨，可看成新的下降趋势，卖出。
    tmp1_s = df['high'] - df['low']
    tmp2_s = (df['high'] - df['close'].shift(1)).abs()
    tmp3_s = (df['low'] - df['close'].shift(1)).abs()
    tr = np.max(np.array([tmp1_s, tmp2_s, tmp3_s]), axis=0)  # 三个数列取其大值

    atr = pd.Series(tr).rolling(n, min_periods=1).mean()
    middle = df['close'].ewm(span=n, adjust=False, min_periods=1).mean()

    signal = middle - 2 * atr - df['close']
    df[factor_name] = scale_01(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
