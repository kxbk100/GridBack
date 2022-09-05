#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff


def signal(*args):
    #该指标使用时注意n不能大于过滤K线数量的一半（不是获取K线数据的一半）

    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    """
    N=14
    TYPICAL_PRICE=(HIGH+LOW+CLOSE)/3
    MF=TYPICAL_PRICE*VOLUME
    MF_POS=SUM(IF(TYPICAL_PRICE>=REF(TYPICAL_PRICE,1),M
    F,0),N)
    MF_NEG=SUM(IF(TYPICAL_PRICE<=REF(TYPICAL_PRICE,1),
    MF,0),N)
    MFI=100-100/(1+MF_POS/MF_NEG)
    MFI 指标的计算与 RSI 指标类似，不同的是，其在上升和下跌的条件
    判断用的是典型价格而不是收盘价，且其是对 MF 求和而不是收盘价
    的变化值。MFI 同样可以用来判断市场的超买超卖状态。
    如果 MFI 上穿 80，则产生买入信号；
    如果 MFI 下穿 20，则产生卖出信号。
    """
    df['price'] = (df['high'] + df['low'] + df['close']) / 3  # TYPICAL_PRICE=(HIGH+LOW+CLOSE)/3
    df['MF'] = df['price'] * df['volume']  # MF=TYPICAL_PRICE*VOLUME
    df['pos'] = np.where(df['price'] >= df['price'].shift(1), df['MF'],
                         0)  # IF(TYPICAL_PRICE>=REF(TYPICAL_PRICE,1),MF,0)MF,0),N)
    df['MF_POS'] = df['pos'].rolling(n).sum()
    df['neg'] = np.where(df['price'] <= df['price'].shift(1), df['MF'],
                         0)  # IF(TYPICAL_PRICE<=REF(TYPICAL_PRICE,1),MF,0)
    df['MF_NEG'] = df['neg'].rolling(n).sum()  # MF_NEG=SUM(IF(TYPICAL_PRICE<=REF(TYPICAL_PRICE,1),MF,0),N)

    df[factor_name] = 100 - 100 / (1 + df['MF_POS'] / df['MF_NEG'])  # MFI=100-100/(1+MF_POS/MF_NEG)


    # 删除中间数据
    del df['price']
    del df['MF']
    del df['pos']
    del df['MF_POS']
    del df['neg']
    del df['MF_NEG']







    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
