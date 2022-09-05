#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
from utils.diff import add_diff, eps


def signal(*args):
    # Rsih
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # CLOSE_DIFF_POS=IF(CLOSE>REF(CLOSE,1),CLOSE-REF(CLOSE,1),0)
    df['close_diff_pos'] = np.where(df['close'] > df['close'].shift(
        1), df['close'] - df['close'].shift(1), 0)
    # sma_diff_pos = df['close_diff_pos'].rolling(n, min_periods=1).mean()
    sma_diff_pos = df['close_diff_pos'].ewm(
        span=n).mean()  # SMA(CLOSE_DIFF_POS,N1,1)
    # abs_sma_diff_pos = abs(df['close'] - df['close'].shift(1)).rolling(n, min_periods=1).mean()
    # SMA(ABS(CLOSE-REF(CLOSE,1)),N1,1
    abs_sma_diff_pos = abs(
        df['close'] - df['close'].shift(1)).ewm(span=n).mean()
    # RSI=SMA(CLOSE_DIFF_POS,N1,1)/SMA(ABS(CLOSE-REF(CLOSE,1)),N1,1)*100
    df['RSI'] = sma_diff_pos / abs_sma_diff_pos * 100
    # RSI_SIGNAL=EMA(RSI,N2)
    df['RSI_ema'] = df['RSI'].ewm(4 * n, adjust=False).mean()
    # RSIH=RSI-RSI_SIGNAL
    df[factor_name] = df['RSI'] - df['RSI_ema']

    # 删除中间过程数据
    del df['close_diff_pos']
    del df['RSI']
    del df['RSI_ema']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
