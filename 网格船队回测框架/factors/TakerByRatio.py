#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff


def signal(*args):
    # TakerByRatio
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    volume = df['quote_volume'].rolling(n, min_periods=1).sum()
    buy_volume = df['taker_buy_quote_asset_volume'].rolling(
        n, min_periods=1).sum()
    df[factor_name] = buy_volume / volume

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
