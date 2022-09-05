#!/usr/bin/python3
# -*- coDing: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # Adx 指标
    """
    N1=14
    MAX_HIGH=IF(HIGH>REF(HIGH,1),HIGH-REF(HIGH,1),0)
    MAX_LOW=IF(REF(LOW,1)>LOW,REF(LOW,1)-LOW,0)
    XPDM=IF(MAX_HIGH>MAX_LOW,HIGH-REF(HIGH,1),0)
    PDM=SUM(XPDM,N1)
    XNDM=IF(MAX_LOW>MAX_HIGH,REF(LOW,1)-LOW,0)
    NDM=SUM(XNDM,N1)
    TR=MAX([ABS(HIGH-LOW),ABS(HIGH-CLOSE),ABS(LOW-CLOSE)])
    TR=SUM(TR,N1)
    Di+=PDM/TR
    Di-=NDM/TR
    Adx 指标计算过程中的 Di+与 Di-指标用相邻两天的最高价之差与最
    低价之差来反映价格的变化趋势。当 Di+上穿 Di-时，产生买入信号；
    当 Di+下穿 Di-时，产生卖出信号。
    """
    max_high = np.where(df['high'] > df['high'].shift(1), df['high'] - df['high'].shift(1), 0)
    max_low = np.where(df['low'].shift(1) > df['low'], df['low'].shift(1) - df['low'], 0)
    xpdm = np.where(pd.Series(max_high) > pd.Series(max_low), pd.Series(max_high) - pd.Series(max_high).shift(1), 0)
    xndm = np.where(pd.Series(max_low) > pd.Series(max_high), pd.Series(max_low).shift(1) - pd.Series(max_low), 0)
    tr = np.max(np.array([
        (df['high'] - df['low']).abs(),
        (df['high'] - df['close']).abs(),
        (df['low'] - df['close']).abs()
    ]), axis=0)  # 三个数列取其大值
    pdm = pd.Series(xpdm).rolling(n, min_periods=1).sum()
    ndm = pd.Series(xndm).rolling(n, min_periods=1).sum()

    di_pos = pd.Series(pdm / pd.Series(tr).rolling(n, min_periods=1).sum())
    di_neg = pd.Series(ndm / pd.Series(tr).rolling(n, min_periods=1).sum())

    adxr = di_pos - di_neg
    df[factor_name] = 0.5 * pd.Series(adxr) + 0.5 * pd.Series(adxr).shift(n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df



