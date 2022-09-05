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
    # Hullma 指标
    """
    N=20,80
    X=2*EMA(CLOSE,[N/2])-EMA(CLOSE,N)
    Hullma=EMA(X,[√𝑁])
    Hullma 也是均线的一种，相比于普通均线有着更低的延迟性。我们
    用短期均线上/下穿长期均线来产生买入/卖出信号。
    """
    _x = 2 * df['close'].ewm(span=int(n / 2), adjust=False, min_periods=1).mean() - df['close'].ewm(
        span=n, adjust=False, min_periods=1).mean()
    hullma = _x.ewm(span=int(np.sqrt(n)), adjust=False, min_periods=1).mean()

    signal = _x - hullma
    df[factor_name] = scale_01(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
