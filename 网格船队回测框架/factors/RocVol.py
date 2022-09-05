#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # RocVol 指标
    """
    N = 80
    RocVol=(VOLUME-REF(VOLUME,N))/REF(VOLUME,N)
    RocVol 是 ROC 的成交量版本。如果 RocVol 上穿 0 则买入，下
    穿 0 则卖出。
    """
    df[factor_name] = df['volume'] / df['volume'].shift(n) - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df