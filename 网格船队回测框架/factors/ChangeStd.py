#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # ChangeStd
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    rtn = df['close'].pct_change()
    df[factor_name] = df['close'].pct_change(n) * rtn.rolling(n).std(ddof=0)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
