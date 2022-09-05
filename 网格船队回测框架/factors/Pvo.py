#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # Pvo
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['emap_1'] = df['volume'].ewm(n, min_periods=1).mean()
    df['emap_2'] = df['volume'].ewm(n * 2, min_periods=1).mean()
    df[factor_name] = (df['emap_1'] - df['emap_2']) / df['emap_2']
    
    del df['emap_1']
    del df['emap_2']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
