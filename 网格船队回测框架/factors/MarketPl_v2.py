#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # MarketPl_v2指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    quote_volume_ema = df['quote_volume'].ewm(span=n, adjust=False).mean()
    volume_ema = df['volume'].ewm(span=n, adjust=False).mean()
    cost = (df['open'] + df['low'] + df['close']) / 3
    cost_ema = cost.ewm(span=n, adjust=False).mean()
    condition = df['quote_volume'] > 0
    df.loc[condition, 'avg_p'] = df['quote_volume'] / df['volume']
    condition = df['quote_volume'] == 0
    df.loc[condition, 'avg_p'] = df['close'].shift(1)
    condition1 = df['avg_p'] <= df['high']
    condition2 = df['avg_p'] >= df['low']
    df.loc[condition1 & condition2, '平均持仓成本'] = quote_volume_ema / volume_ema
    condition1 = df['avg_p'] > df['high']
    condition2 = df['avg_p'] < df['low']
    df.loc[condition1 & condition2, '平均持仓成本'] = cost_ema
    df[factor_name] = df['close'] / (df['平均持仓成本'] + eps) - 1

    del df['平均持仓成本']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
