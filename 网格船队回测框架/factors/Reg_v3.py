#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import talib as ta
from utils.diff import add_diff, eps
from sklearn.linear_model import LinearRegression


def signal(*args):
    # Reg_v3    
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    # sklearn 线性回归
    def reg_ols(_y):
        _x = np.arange(n) + 1
        model = LinearRegression().fit(_x.reshape(-1, 1), _y)  # 线性回归训练
        y_pred = model.coef_ * _x + model.intercept_  # y = ax + b
        return y_pred[-1]

    df['reg_close'] = df['close'].rolling(n).apply(
        lambda y: reg_ols(y), raw=False)
    df[factor_name] = df['close'] / (df['reg_close'] + eps) - 1
    
    # 删除多余列
    del df['reg_close']
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
