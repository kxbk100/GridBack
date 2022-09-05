#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff


def signal(*args):
    # SrocVol 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # EMAP=EMA(VOLUME,N)
    df['emap'] = df['volume'].ewm(2 * n, adjust=False).mean()
    # SROCVOL=(EMAP-REF(EMAP,M))/REF(EMAP,M)
    df[factor_name] = (df['emap'] - df['emap'].shift(n)) / df['emap'].shift(n)

    del df['emap']
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
