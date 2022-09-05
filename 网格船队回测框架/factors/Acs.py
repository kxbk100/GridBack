#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Acs 指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['adx'] = ta.ADX(df['high'], df['low'], df['close'], n)
    df['adx_close'] = df['adx'] / df['close']
    df[factor_name] = df['adx_close'].rolling(n).std()

    del df['adx'], df['adx_close']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
