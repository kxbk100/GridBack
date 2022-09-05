#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # Rsi
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    diff = df['close'].diff()  # CLOSE-REF(CLOSE,1) 计算当前close 与前一周期的close的差值
    # IF(CLOSE>REF(CLOSE,1),CLOSE-REF(CLOSE,1),0) 表示当前是上涨状态，记录上涨幅度
    df['up'] = np.where(diff > 0, diff, 0)
    # IF(CLOSE<REF(CLOSE,1),ABS(CLOSE-REF(CLOSE,1)),0) 表示当前为下降状态，记录下降幅度
    df['down'] = np.where(diff < 0, abs(diff), 0)
    A = df['up'].ewm(span=n).mean()  # SMA(CLOSEUP,N,1) 计算周期内的上涨幅度的sma
    B = df['down'].ewm(span=n).mean()  # SMA(CLOSEDOWN,N,1)计算周期内的下降幅度的sma
    # RSI=100*CLOSEUP_MA/(CLOSEUP_MA+CLOSEDOWN_MA)  没有乘以100   没有量纲即可
    df[factor_name] = A / (A + B + eps)

    # 删除多余列
    del df['up'], df['down']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
