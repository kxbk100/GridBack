#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff, eps


def signal(*args):
    # Cmo
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # MAX(CLOSE-REF(CLOSE,1), 0
    df['max_su'] = np.where(df['close'] > df['close'].shift(
        1), df['close'] - df['close'].shift(1), 0)
    # SU=SUM(MAX(CLOSE-REF(CLOSE,1),0),N)
    df['sum_su'] = df['max_su'].rolling(n, min_periods=1).sum()
    # MAX(REF(CLOSE,1)-CLOSE,0)
    df['max_sd'] = np.where(df['close'].shift(
        1) > df['close'], df['close'].shift(1) - df['close'], 0)
    # SD=SUM(MAX(REF(CLOSE,1)-CLOSE,0),N)
    df['sum_sd'] = df['max_sd'].rolling(n, min_periods=1).sum()
    # CMO=(SU-SD)/(SU+SD)*100
    df[factor_name] = (df['sum_su'] - df['sum_sd']) / \
        (df['sum_su'] + df['sum_sd'] + eps) * 100

    # 删除多余列
    del df['max_su'], df['sum_su'], df['max_sd'], df['sum_sd']
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
