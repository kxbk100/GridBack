#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff



def signal(*args):

    # PVI 指标
    """
    N=40
    PVI_INC=IF(VOLUME>REF(VOLUME,1),(CLOSE-REF(CLOSE))/
    CLOSE,0)
    PVI=CUM_SUM(PVI_INC)
    PVI_MA=MA(PVI,N)
    PVI 是成交量升高的交易日的价格变化百分比的累积。
    PVI 相关理论认为，如果当前价涨量增，则说明散户主导市场，PVI
    可以用来识别价涨量增的市场（散户主导的市场）。
    如果 PVI 上穿 PVI_MA，则产生买入信号；
    如果 PVI 下穿 PVI_MA，则产生卖出信号。
    """

    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['ref_close'] = (df['close'] - df['close'].shift(1)) / df['close']
    df['PVI_INC'] = np.where(df['volume'] > df['volume'].shift(1), df['ref_close'], 0)
    df['PVI'] = df['PVI_INC'].cumsum()
    df[factor_name] = df['PVI'].rolling(n, min_periods=1).mean()

    del df['ref_close']
    del df['PVI_INC']
    del df['PVI']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
