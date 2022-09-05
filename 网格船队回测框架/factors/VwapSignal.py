#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # VwapSignal指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    """
    # N=20
    # Typical=(HIGH+LOW+CLOSE)/3
    # MF=VOLUME*Typical
    # VOLUME_SUM=SUM(VOLUME,N)
    # MF_SUM=SUM(MF,N)
    # VWAP=MF_SUM/VOLUME_SUM
    # VWAP以成交量为权重计算价格的加权平均。如果当前价格上穿VWAP，则买入；如果当前价格下穿VWAP，则卖出。
    """
    df['tp'] = df[['high', 'low', 'close']].sum(axis=1) / 3
    df['mf'] = df['volume'] * df['tp']
    df['vol_sum'] = df['volume'].rolling(n, min_periods=1).sum()
    df['mf_sum'] = df['mf'].rolling(n, min_periods=1).sum()
    df['vwap'] = df['mf_sum'] / (eps + df['vol_sum'])
    df[factor_name] = df['tp'] / (df['vwap'] + eps) - 1

    # 删除多余列
    del df['tp'], df['mf'], df['vol_sum'], df['mf_sum'], df['vwap']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
