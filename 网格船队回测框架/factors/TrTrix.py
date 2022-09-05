#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # TrTrix 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['tr_trix'] = df['close'].ewm(span=n, adjust=False).mean()
    df[factor_name] = df['tr_trix'].pct_change()

    # 删除多余列
    del df['tr_trix']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
