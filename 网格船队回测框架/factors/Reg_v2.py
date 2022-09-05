#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Reg_v2    
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    df['LINEARREG'] = ta.LINEARREG(df['close'], timeperiod=2 * n)
    df[factor_name] = 100 * (df['close'] - df['LINEARREG']) / (df['LINEARREG'] + eps)

    # 删除多余列
    del df['LINEARREG']
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
