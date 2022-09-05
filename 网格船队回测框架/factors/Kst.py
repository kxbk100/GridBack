#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    # KST 指标
    """
    ROC_MA1=MA(CLOSE-REF(CLOSE,10),10)
    ROC_MA2=MA(CLOSE -REF(CLOSE,15),10)
    ROC_MA3=MA(CLOSE -REF(CLOSE,20),10)
    ROC_MA4=MA(CLOSE -REF(CLOSE,30),10)
    KST_IND=ROC_MA1+ROC_MA2*2+ROC_MA3*3+ROC_MA4*4
    KST=MA(KST_IND,9)
    KST 结合了不同时间长度的 ROC 指标。如果 KST 上穿/下穿 0 则产
    生买入/卖出信号。
    """
    df['ROC1'] = df['close'] - df['close'].shift(n)
    df['ROC_MA1'] = df['ROC1'].rolling(n, min_periods=1).mean()
    df['ROC2'] = df['close'] - df['close'].shift(int(n * 1.5))
    df['ROC_MA2'] = df['ROC2'].rolling(n, min_periods=1).mean()
    df['ROC3'] = df['close'] - df['close'].shift(int(n * 2))
    df['ROC_MA3'] = df['ROC3'].rolling(n, min_periods=1).mean()
    df['ROC4'] = df['close'] - df['close'].shift(int(n * 3))
    df['ROC_MA4'] = df['ROC4'].rolling(n, min_periods=1).mean()
    df['KST_IND'] = df['ROC_MA1'] + df['ROC_MA2'] * 2 + df['ROC_MA3'] * 3 + df['ROC_MA4'] * 4
    df['KST'] = df['KST_IND'].rolling(n, min_periods=1).mean()
    # 去量纲
    df[factor_name] = df['KST_IND'] / df['KST']

    del df['ROC1']
    del df['ROC_MA1']
    del df['ROC2']
    del df['ROC_MA2']
    del df['ROC3']
    del df['ROC_MA3']
    del df['ROC4']
    del df['ROC_MA4']
    del df['KST_IND']
    del df['KST']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df