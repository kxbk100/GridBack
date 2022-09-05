#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Tema_v2指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['TEMA'] = ta.TEMA(df['close'], timeperiod=2 * n)
    df[factor_name] = 100 * (df['close'] - df['TEMA']) / (df['TEMA'] + eps)

    del df['TEMA']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
