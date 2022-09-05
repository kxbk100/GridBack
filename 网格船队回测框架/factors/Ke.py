#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Ke指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    volume_avg = df['volume'].rolling(n).mean()
    volume_stander = df['volume'] / volume_avg
    price_change = df['close'].pct_change(n)
    df[factor_name] = (price_change / (abs(price_change) + eps)) * \
        volume_stander * price_change ** 2

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
