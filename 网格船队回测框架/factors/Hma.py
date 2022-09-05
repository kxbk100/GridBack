#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff,eps


def signal(*args):
    # Hma
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    df[factor_name] = df['high'].rolling(n, min_periods=1).mean()

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
