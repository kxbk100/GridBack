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
    # RVI 指标
    """
    N1=10
    N2=20
    STD=STD(CLOSE,N)
    USTD=SUM(IF(CLOSE>REF(CLOSE,1),STD,0),N2)
    DSTD=SUM(IF(CLOSE<REF(CLOSE,1),STD,0),N2)
    RVI=100*USTD/(USTD+DSTD)
    RVI 的计算方式与 RSI 一样，不同的是将 RSI 计算中的收盘价变化值
    替换为收盘价在过去一段时间的标准差，用来反映一段时间内上升
    的波动率和下降的波动率的对比。我们也可以像计算 RSI 指标时一样
    先对公式中的 USTD 和 DSTD 作移动平均得到 USTD_MA 和
    DSTD_MA 再求出 RVI=100*USTD_MV/(USTD_MV+DSTD_MV)。
    RVI 的用法与 RSI 一样。通常认为当 RVI 大于 70，市场处于强势上
    涨甚至达到超买的状态；当 RVI 小于 30，市场处于强势下跌甚至达
    到超卖的状态。当 RVI 跌到 30 以下又上穿 30 时，通常认为股价要
    从超卖的状态反弹；当 RVI 超过 70 又下穿 70 时，通常认为市场要
    从超买的状态回落了。
    如果 RVI 上穿 30，则产生买入信号；
    如果 RVI 下穿 70，则产生卖出信号。
    """
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)
    df['ustd'] = np.where(df['close'] > df['close'].shift(1), df['std'], 0)
    df['sum_ustd'] = df['ustd'].rolling(2 * n).sum()

    df['dstd'] = np.where(df['close'] < df['close'].shift(1), df['std'], 0)
    df['sum_dstd'] = df['dstd'].rolling(2 * n).sum()

    df[factor_name] = df['sum_ustd'] / (df['sum_ustd'] + df['sum_dstd']) * 100
    
    del df['std']
    del df['ustd']
    del df['sum_ustd']
    del df['dstd']
    del df['sum_dstd']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df





