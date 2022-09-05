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
    # ******************** FbUpperSignal 指标 ********************
    # N=20
    # TR=MAX(HIGH-LOW,ABS(HIGH-REF(CLOSE,1)),ABS(LOW-REF(CLOSE,1)))
    # ATR=MA(TR,N)
    # MIDDLE=MA(CLOSE,N)
    # UPPER1=MIDDLE+1.618*ATR
    # UPPER2=MIDDLE+2.618*ATR
    # UPPER3=MIDDLE+4.236*ATR
    # LOWER1=MIDDLE-1.618*ATR
    # LOWER2=MIDDLE-2.618*ATR
    # LOWER3=MIDDLE-4.236*ATR
    # FB指标类似于布林带，都以价格的移动平均线为中轨，在中线上下浮动一定数值构造上下轨。
    # 不同的是，Fibonacci Bands有三条上轨和三条下轨，且分别为中轨加减ATR乘Fibonacci因子所得。
    # 当收盘价突破较高的两个上轨的其中之一时，产生买入信号；收盘价突破较低的两个下轨的其中之一时，产生卖出信号。
    tmp1_s = df['high'] - df['low']
    tmp2_s = (df['high'] - df['close'].shift(1)).abs()
    tmp3_s = (df['low'] - df['close'].shift(1)).abs()

    tr = np.max(np.array([tmp1_s, tmp2_s, tmp3_s]), axis=0)  # 三个数列取其大值

    atr = pd.Series(tr).rolling(n, min_periods=1).mean()
    middle = df['close'].rolling(n, min_periods=1).mean()

    signal = df['close'] - middle - 2.618 * atr
    df[factor_name] = scale_01(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
