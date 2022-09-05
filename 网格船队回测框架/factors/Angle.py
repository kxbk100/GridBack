#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps
import talib as ta


def signal(*args):
    # AvgPrice
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df[factor_name] = ta.LINEARREG_ANGLE(df['close'], timeperiod=n)

    # 删除多余列


    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
