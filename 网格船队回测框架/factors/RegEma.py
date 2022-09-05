#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # RegEma
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    ema = df['close'].ewm(span=n, adjust=False, min_periods=1).mean()
    reg_close = ta.LINEARREG(ema, timeperiod=n)
    df[factor_name] = df['close'] / (reg_close + eps) - 1
        
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
