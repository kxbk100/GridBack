#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Pac 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    """
    N1=20
    N2=20
    UPPER=SMA(HIGH,N1,1)
    LOWER=SMA(LOW,N2,1)
    用最高价和最低价的移动平均来构造价格变化的通道，如果价格突破
    上轨则做多，突破下轨则做空。
    """
    df['upper'] = df['high'].ewm(span=n).mean()  # UPPER=SMA(HIGH,N1,1)
    df['lower'] = df['low'].ewm(span=n).mean()  # LOWER=SMA(LOW,N2,1)
    df['width'] = df['upper'] - df['lower']  # 添加指标求宽度进行去量纲
    df['width_ma'] = df['width'].rolling(n, min_periods=1).mean()

    df[factor_name] = df['width'] / (df['width_ma'] + eps) - 1

    # 删除多余列
    del df['upper'], df['lower'], df['width'], df['width_ma']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
