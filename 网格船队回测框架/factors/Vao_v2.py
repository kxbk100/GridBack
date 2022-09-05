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
    # PVT 指标
    """
    PVT=(CLOSE-REF(CLOSE,1))/REF(CLOSE,1)*VOLUME
    PVT_MA1=MA(PVT,N1)
    PVT_MA2=MA(PVT,N2)
    PVT 指标用价格的变化率作为权重求成交量的移动平均。PVT 指标
    与 OBV 指标的思想类似，但与 OBV 指标相比，PVT 考虑了价格不
    同涨跌幅的影响，而 OBV 只考虑了价格的变化方向。我们这里用 PVT
    短期和长期均线的交叉来产生交易信号。
    如果 PVT_MA1 上穿 PVT_MA2，则产生买入信号；
    如果 PVT_MA1 下穿 PVT_MA2，则产生卖出信号。
    """
    df['WV'] = df['volume'] * (df['close'] - 0.5 * df['high'] - 0.5 * df['low'])
    df['VAO'] = df['WV']+df['WV'].shift(1)
    df['VAO_MA1'] = df['VAO'].rolling(n, min_periods=1).mean()
    df['VAO_MA2'] = df['VAO'].rolling(3 * n, min_periods=1).mean()
    df['Vao_v2'] = df['VAO_MA1'] - df['VAO_MA2']

    # 去量纲
    df[factor_name] = df['VAO'] / df['Vao_v2'] - 1

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df