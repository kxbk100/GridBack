#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff, eps


def signal(*args):
    # Cmo_v3
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['momentum'] = df['close'] - df['close'].shift(1)
    df['up'] = np.where(df['momentum'] > 0, df['momentum'], 0)
    df['dn'] = np.where(df['momentum'] < 0, abs(df['momentum']), 0)
    df['up_sum'] = df['up'].rolling(window=n, min_periods=1).sum()
    df['dn_sum'] = df['dn'].rolling(window=n, min_periods=1).sum()
    df['cmo'] = (
        df['up_sum'] - df['dn_sum']) / (df['up_sum'] + df['dn_sum'] + eps) * 100
    df[factor_name] = df['cmo'].rolling(window=n, min_periods=1).mean()

    # 删除多余列
    del df['momentum'], df['up'], df['dn'], df['up_sum'], df['dn_sum'], df['cmo']
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
