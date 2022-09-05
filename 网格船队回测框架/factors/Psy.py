#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff, eps


def signal(*args):
    # Psy
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    df['P'] = np.where(df['close'] > df['close'].shift(1), 1, 0)  # IF(CLOSE>REF(CLOSE,1),1,0)
    df[factor_name] = df['P'] / n * 100  # PSY=IF(CLOSE>REF(CLOSE,1),1,0)/N*100

    # 删除多余列
    del df['P']
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
