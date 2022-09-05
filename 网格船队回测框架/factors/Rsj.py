#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff, eps


def signal(*args):
    # Rsj 指标
    
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # 计算收益率
    df['return'] = df['close'] / df['close'].shift(1) - 1

    # 计算RV
    df['pow_return'] = pow(df['return'], 2)
    df['rv'] = df['pow_return'].rolling(window=n, min_periods=1).sum()

    # 计算RV +/-
    df['positive_data'] = np.where(df['return'] > 0, df['return'], 0)
    df['negative_data'] = np.where(df['return'] < 0, df['return'], 0)
    df['pow_positive_data'] = pow(df['positive_data'], 2)
    df['pow_negetive_data'] = pow(df['negative_data'], 2)
    df['rv+'] = df['pow_positive_data'].rolling(window=n, min_periods=1).sum()
    df['rv-'] = df['pow_negetive_data'].rolling(window=n, min_periods=1).sum()

    # 计算RSJ
    df[factor_name] = (df['rv+'] - df['rv-']) / (df['rv'] + eps)

    # 删除多余列
    del df['return'], df['rv'], df['positive_data'], df['negative_data']
    del df['rv+'], df['rv-'], df['pow_positive_data'], df['pow_negetive_data']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
