#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff,eps


def signal(*args):
    # Tma
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    df['ma'] = df['close'].rolling(n, min_periods=1).mean()
    df['ma2'] = df['ma'].rolling(n, min_periods=1).mean()
    df[factor_name] = df['close'] / (df['ma2'] + eps) - 1

    # 删除多余列
    del df['ma'], df['ma2']
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
