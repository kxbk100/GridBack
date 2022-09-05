#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Er 指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    a = 2 / (n + 1)
    df['ema'] = df['close'].ewm(alpha=a, adjust=False).mean()
    df['BullPower'] = (df['high'] - df['ema']) / df['ema']
    df['BearPower'] = (df['low'] - df['ema']) / df['ema']
    df[factor_name] = df['BullPower'] + df['BearPower']

    # 删除多余列
    del df['ema'], df['BullPower'], df['BearPower']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
