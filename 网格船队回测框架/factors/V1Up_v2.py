#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff,eps


def signal(*args):
    # V1Up_v2 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    n1 = n

    # 计算动量因子
    mtm = df['close'] / df['close'].shift(n1) - 1
    mtm_mean = mtm.rolling(window=n1, min_periods=1).mean()

    # 基于价格atr，计算波动率因子wd_atr
    c1 = df['high'] - df['low']
    c2 = abs(df['high'] - df['close'].shift(1))
    c3 = abs(df['low'] - df['close'].shift(1))
    tr = np.max(np.array([c1, c2, c3]), axis=0)  # 三个数列取其大值
    atr = pd.Series(tr).rolling(window=n1, min_periods=1).mean()
    avg_price = df['close'].rolling(window=n1, min_periods=1).mean()
    wd_atr = atr / avg_price  # === 波动率因子

    # 参考ATR，对MTM指标，计算波动率因子
    mtm_l = df['low'] / df['low'].shift(n1) - 1
    mtm_h = df['high'] / df['high'].shift(n1) - 1
    mtm_c = df['close'] / df['close'].shift(n1) - 1
    mtm_c1 = mtm_h - mtm_l
    mtm_c2 = abs(mtm_h - mtm_c.shift(1))
    mtm_c3 = abs(mtm_l - mtm_c.shift(1))
    mtm_tr = np.max(
        np.array([mtm_c1, mtm_c2, mtm_c3]), axis=0)  # 三个数列取其大值
    mtm_atr = pd.Series(mtm_tr).rolling(
        window=n1, min_periods=1).mean()  # === mtm 波动率因子

    # 参考ATR，对MTM mean指标，计算波动率因子
    mtm_l_mean = mtm_l.rolling(window=n1, min_periods=1).mean()
    mtm_h_mean = mtm_h.rolling(window=n1, min_periods=1).mean()
    mtm_c_mean = mtm_c.rolling(window=n1, min_periods=1).mean()
    mtm_c1 = mtm_h_mean - mtm_l_mean
    mtm_c2 = abs(mtm_h_mean - mtm_c_mean.shift(1))
    mtm_c3 = abs(mtm_l_mean - mtm_c_mean.shift(1))
    mtm_tr = np.max(
        np.array([mtm_c1, mtm_c2, mtm_c3]), axis=0)  # 三个数列取其大值
    mtm_atr_mean = pd.Series(mtm_tr).rolling(
        window=n1, min_periods=1).mean()  # === mtm_mean 波动率因子

    indicator = mtm_mean
    # mtm_mean指标分别乘以三个波动率因子
    indicator *= wd_atr * mtm_atr * mtm_atr_mean
    indicator = pd.Series(indicator)

    # 对新策略因子计算自适应布林
    median = indicator.rolling(window=n1).mean()
    std = indicator.rolling(n1, min_periods=1).std(
        ddof=0)  # ddof代表标准差自由度
    z_score = abs(indicator - median) / std
    m1 = pd.Series(z_score).rolling(window=n1).mean()
    up1 = median + std * m1
    indicator *= 1e8
    up1 *= 1e8
    df[factor_name] = up1 - indicator

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
