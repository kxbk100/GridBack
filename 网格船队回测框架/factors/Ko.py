#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Ko指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['price'] = (df['high'] + df['low'] + df['close']) / 3
    df['V'] = np.where(df['price'] > df['price'].shift(1), df['volume'], -df['volume'])
    df['V_ema1'] = df['V'].ewm(n, adjust=False).mean()
    df['V_ema2'] = df['V'].ewm(int(n * 1.618), adjust=False).mean()
    df['KO'] = df['V_ema1'] - df['V_ema2']
    # 标准化
    df[factor_name] = (df['KO'] - df['KO'].rolling(n).min()) / (
        df['KO'].rolling(n).max() - df['KO'].rolling(n).min() + eps)

    # 删除多余列
    del df['price'], df['V'], df['V_ema1'], df['V_ema2'], df['KO']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
