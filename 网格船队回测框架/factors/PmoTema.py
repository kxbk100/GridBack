#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    # PmoTema 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # TEMA均线
    df['ema'] = df['close'].ewm(n, adjust=False).mean()
    df['ema_ema'] = df['ema'].ewm(n, adjust=False).mean()
    df['ema_ema_ema'] = df['ema_ema'].ewm(n, adjust=False).mean()
    df['TEMA'] = 3 * df['ema'] - 3 * df['ema_ema'] + df['ema_ema_ema']

    # 计算PMO
    df['ROC'] = (df['TEMA'] - df['TEMA'].shift(1)) / \
        df['TEMA'].shift(1) * 100  # 用TEMA均线代替原CLOSE
    df['ROC_MA'] = df['ROC'].rolling(
        n, min_periods=1).mean()  # 均线代替动态移动平均
    df['ROC_MA10'] = df['ROC_MA'] * 10
    df['PMO'] = df['ROC_MA10'].rolling(4 * n, min_periods=1).mean()
    df[factor_name] = df['PMO'].rolling(2 * n, min_periods=1).mean()

    del df['ema'], df['ema_ema'], df['ema_ema_ema'], df['TEMA']
    del df['ROC'], df['ROC_MA']
    del df['ROC_MA10']
    del df['PMO']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df





    
