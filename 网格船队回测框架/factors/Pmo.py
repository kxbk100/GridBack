#!/usr/bin/python3
# -*- coding: utf-8 -*-


import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    # PMO 指标
    """
    N1=10
    N2=40
    N3=20
    ROC=(CLOSE-REF(CLOSE,1))/REF(CLOSE,1)*100
    ROC_MA=DMA(ROC,2/N1)
    ROC_MA10=ROC_MA*10
    PMO=DMA(ROC_MA10,2/N2)
    PMO_SIGNAL=DMA(PMO,2/(N3+1))
    PMO 指标是 ROC 指标的双重平滑（移动平均）版本。与 SROC 不 同(SROC 是先对价格作平滑再求 ROC)，而 PMO 是先求 ROC 再对
    ROC 作平滑处理。PMO 越大（大于 0），则说明市场上涨趋势越强；
    PMO 越小（小于 0），则说明市场下跌趋势越强。如果 PMO 上穿/
    下穿其信号线，则产生买入/卖出指标。
    """
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['ROC'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1) * 100
    df['ROC_MA'] = df['ROC'].rolling(n, min_periods=1).mean()
    df['ROC_MA10'] = df['ROC_MA'] * 10
    df['PMO'] = df['ROC_MA10'].rolling(4 * n, min_periods=1).mean()
    df[factor_name] = df['PMO'].rolling(2 * n, min_periods=1).mean()

    del df['ROC']
    del df['ROC_MA']
    del df['ROC_MA10']
    del df['PMO']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df





    