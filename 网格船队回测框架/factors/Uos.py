#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff


def signal(*args):
    # Uos指标
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    M = n
    N = 2 * n
    O = 4 * n
    df['ref_close'] = df['close'].shift(1)
    df['TH'] = df[['high', 'ref_close']].max(axis=1)
    df['TL'] = df[['low', 'ref_close']].min(axis=1)
    df['TR'] = df['TH'] - df['TL']
    df['XR'] = df['close'] - df['TL']
    df['XRM'] = df['XR'].rolling(M).sum() / df['TR'].rolling(M).sum()
    df['XRN'] = df['XR'].rolling(N).sum() / df['TR'].rolling(N).sum()
    df['XRO'] = df['XR'].rolling(O).sum() / df['TR'].rolling(O).sum()
    df[factor_name] = 100 * (df['XRM'] * N * O + df['XRN'] * M * O + df['XRO'] * M * N) / (M * N + M * O + N * O)

    # 删除多余列
    del df['ref_close'], df['TH'], df['TL'], df['TR'], df['XR']
    del df['XRM'], df['XRN'], df['XRO']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
