#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # MarketPl指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    quote_volume_ema = df['quote_volume'].ewm(span=n, adjust=False).mean()
    volume_ema = df['volume'].ewm(span=n, adjust=False).mean()
    df['平均持仓成本'] = quote_volume_ema / volume_ema
    df[factor_name] = df['close'] / (df['平均持仓成本'] + eps) - 1

    del df['平均持仓成本']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
