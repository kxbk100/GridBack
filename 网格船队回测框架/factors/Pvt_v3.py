#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Pvt_v3 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    pvt = (df['volume'] * (df['close'] - df['close'].shift(1)) /
           df['close'].shift(1)).rolling(n, min_periods=1).sum()
    pvt_ma1 = pd.Series(pvt).rolling(n, min_periods=1).mean()
    pvt_ma2 = pd.Series(pvt).rolling(2 * n, min_periods=1).mean()
    df[factor_name] = pd.Series(pvt_ma1 - pvt_ma2)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
