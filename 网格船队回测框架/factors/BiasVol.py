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

    # BIASVOL 指标
    """
    N=6，12，24
    BIASVOL(N)=(VOLUME-MA(VOLUME,N))/MA(VOLUME,N)
    BIASVOL 是乖离率 BIAS 指标的成交量版本。如果 BIASVOL6 大于
    5 且 BIASVOL12 大于 7 且 BIASVOL24 大于 11，则产生买入信号；
    如果 BIASVOL6 小于-5 且 BIASVOL12 小于-7 且 BIASVOL24 小于
    -11，则产生卖出信号。
    """
    df['ma_volume'] = df['volume'].rolling(n, min_periods=1).mean()
    df[factor_name] = (df['volume'] - df['ma_volume']) / df['ma_volume']

    del df['ma_volume']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

