#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff, eps


def signal(*args):
    # Sroc
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    """
    N=13
    M=21
    EMAP=EMA(CLOSE,N)
    SROC=(EMAP-REF(EMAP,M))/REF(EMAP,M)
    SROC 与 ROC 类似，但是会对收盘价进行平滑处理后再求变化率。
    """
    ema = df['close'].ewm(n, adjust=False).mean()
    ref = ema.shift(2 * n)
    df[factor_name] = (ema - ref) / (ref + eps)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
