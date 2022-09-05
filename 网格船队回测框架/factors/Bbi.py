#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff,eps


def signal(*args):
    # Bbi
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    """
    BBI=(MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4
    BBI 是对不同时间长度的移动平均线取平均，能够综合不同移动平均
    线的平滑性和滞后性。如果收盘价上穿/下穿 BBI 则产生买入/卖出信
    号。
    """
    # 将BBI指标计算出来求bias
    ma1 = df['close'].rolling(n, min_periods=1).mean()
    ma2 = df['close'].rolling(2 * n, min_periods=1).mean()
    ma3 = df['close'].rolling(4 * n, min_periods=1).mean()
    ma4 = df['close'].rolling(8 * n, min_periods=1).mean()
    # BBI=(MA(CLOSE,3)+MA(CLOSE,6)+MA(CLOSE,12)+MA(CLOSE,24))/4
    bbi = (ma1 + ma2 + ma3 + ma4) / 4
    df[factor_name] = bbi / df['close']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
