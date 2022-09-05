#!/usr/bin/python3
# -*- coding: utf-8 -*-
import numpy  as np
import talib
import pandas as pd
from utils.diff import add_diff

def signal(*args):
    # ******************** KAMA ********************
    # N=10
    # N1=2
    # N2=30
    # DIRECTION=CLOSE-REF(CLOSE,N)
    # VOLATILITY=SUM(ABS(CLOSE-REF(CLOSE,1)),N)
    # ER=DIRETION/VOLATILITY
    # FAST=2/(N1+1)
    # SLOW=2/(N2+1)
    # SMOOTH=ER*(FAST-SLOW)+SLOW
    # COF=SMOOTH*SMOOTH
    # KAMA=COF*CLOSE+(1-COF)*REF(KAMA,1)
    # KAMA指标与VIDYA指标类似，都是把ER(EfficiencyRatio)指标加入到移动平均的权重中，
    # 其用法与其他移动平均线类似。在当前趋势较强时，ER值较大，KAMA会赋予当前价格更大的权重，
    # 使得KAMA紧随价格变动，减小其滞后性；在当前趋势较弱（比如振荡市中）,ER值较小，
    # KAMA会赋予当前价格较小的权重，增大KAMA的滞后性，使其更加平滑，避免产生过多的交易信号。
    # 与VIDYA指标不同的是，KAMA指标可以设置权值的上界FAST和下界SLOW。
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    direction = df['close'] - df['close'].shift(1)
    volatility = (df['close'] - df['close'].shift(1)).abs().rolling(int(10 * n), min_periods=1).mean()
    er = direction / volatility
    fast = 2 / (n / 5 + 1)
    slow = 2 / (3 * n + 1)
    smooth = er * (fast - slow) + slow
    cof = smooth * smooth
    kama = cof * df['close']
    df[factor_name] = kama + (1 - cof) * kama.shift(1)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
