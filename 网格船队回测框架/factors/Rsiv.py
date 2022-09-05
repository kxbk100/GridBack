#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    # RSIV 指标
    """
    N=20
    VOLUP=IF(CLOSE>REF(CLOSE,1),VOLUME,0)
    VOLDOWN=IF(CLOSE<REF(CLOSE,1),VOLUME,0)
    SUMUP=SUM(VOLUP,N)
    SUMDOWN=SUM(VOLDOWN,N)
    RSIV=100*SUMUP/(SUMUP+SUMDOWN)
    RSIV 的计算方式与 RSI 相同，只是把其中的价格变化 CLOSEREF(CLOSE,1)替换成了成交量 VOLUME。用法与 RSI 类似。我们
    这里将其用作动量指标，上穿 60 买入，下穿 40 卖出。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['VOLUP'] = np.where(df['close'] > df['close'].shift(1), df['volume'], 0)
    df['VOLDOWN'] = np.where(df['close'] < df['close'].shift(1), df['volume'], 0)
    df['SUMUP'] = df['VOLUP'].rolling(n).sum()
    df['SUMDOWN'] = df['VOLDOWN'].rolling(n).sum()
    df[factor_name] = df['SUMUP'] / (df['SUMUP'] + df['SUMDOWN']) * 100

    del df['VOLUP']
    del df['VOLDOWN']
    del df['SUMUP']
    del df['SUMDOWN']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
