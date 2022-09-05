#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # RegTema
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    ema = df['close'].ewm(span=n, adjust=False).mean()
    emax2 = ema.ewm(span=n, adjust=False).mean()
    emax3 = emax2.ewm(span=n, adjust=False).mean()
    tema = 3 * ema - 3 * emax2 + emax3

    # 计算reg
    reg_tema = ta.LINEARREG(tema, timeperiod=n)  # 该部分为talib内置求线性回归
    df[factor_name] = tema / (reg_tema + eps) - 1
        
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
