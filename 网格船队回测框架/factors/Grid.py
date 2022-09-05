#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff,eps


def signal(*args):
    # Grid
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    df['median'] = df['close'].rolling(n, min_periods=1).mean()
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)
    df['grid'] = (df['close'] - df['median']) / df['std']
    df['grid'] = df['grid'].replace([np.inf, -np.inf], np.nan)
    df['grid'].fillna(value=0, inplace=True)
    df['grid'] = df['grid'].rolling(window=n).mean()
    df[factor_name] = df['grid'].pct_change(n)
    # df['gridInt'] = df['grid'].astype("int")
    # df[factor_name] = df['gridInt'].pct_change(n)

    del df['median'], df['std'], df['grid']  # , df['gridInt']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
