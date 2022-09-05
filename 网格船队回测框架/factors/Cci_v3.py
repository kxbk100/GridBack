#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Cci_v3 最常用的T指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    oma = df['open'].ewm(span=n, adjust=False).mean()
    hma = df['high'].ewm(span=n, adjust=False).mean()
    lma = df['low'].ewm(span=n, adjust=False).mean()
    cma = df['close'].ewm(span=n, adjust=False).mean()
    tp = (oma + hma + lma + cma) / 4
    ma = tp.ewm(span=n, adjust=False).mean()
    md = (cma - ma).abs().ewm(span=n, adjust=False).mean()
    df[factor_name] = (tp - ma) / (md + eps)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
