#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import talib as ta
from utils.diff import add_diff


def signal(*args):
    # Reg
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    df['reg_close'] = ta.LINEARREG(df['close'], timeperiod=n)  # 该部分为talib内置求线性回归
    df[factor_name] = df['close'] / df['reg_close'] - 1

    # 删除多余列
    del df['reg_close']
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
