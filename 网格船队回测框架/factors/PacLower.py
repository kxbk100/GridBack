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
    # ******************** Pac ********************
    # N1=20
    # N2=20
    # UPPER=SMA(HIGH,N1,1)
    # LOWER=SMA(LOW,N2,1)
    # 用最高价和最低价的移动平均来构造价格变化的通道，如果价格突破上轨则做多，突破下轨则做空。
    lower = df['low'].ewm(alpha=1 / n, adjust=False).mean()
    df[factor_name] = scale_01(lower, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df