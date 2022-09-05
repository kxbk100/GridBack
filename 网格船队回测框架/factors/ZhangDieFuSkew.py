#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff


def signal(*args):
    # ZhangDieFuSkew
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    # 涨跌幅偏度：在商品期货市场有效
    change = df['close'].pct_change()
    df[factor_name] = pd.Series(change).rolling(n).skew()

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
