#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # 计算Macd指标
    ema1 = (0.5 * df['high'] + 0.5 * df['low']).ewm(span=n, adjust=False).mean()
    ema2 = (0.5 * df['high'] + 0.5 * df['low']).ewm(span=2 * n, adjust=False).mean()

    dif = ema1 - ema2
    dea = dif.ewm(span=int(n / 2.), adjust=False).mean()

    df[factor_name] = 10 * (2 * dif - dea)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df