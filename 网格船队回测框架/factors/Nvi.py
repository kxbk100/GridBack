#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff


# =====函数  01归一化
def scale_01(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).min()) / (
            1e-9 + pd.Series(_s).rolling(_n, min_periods=1).max() - pd.Series(_s).rolling(_n, min_periods=1).min()
    )
    return pd.Series(_s)

def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # ******************** Nvi ********************
    # --- NVI --- 099/125
    # N=144
    # NVI_INC=IF(VOLUME<REF(VOLUME,1),1+(CLOSE-REF(CLOSE,1))/CLOSE,1)
    # NVI_INC[0]=100
    # NVI=CUM_PROD(NVI_INC)
    # NVI_MA=MA(NVI,N)
    # NVI是成交量降低的交易日的价格变化百分比的累积。NVI相关理论认为，如果当前价涨量缩，
    # 则说明大户主导市场，NVI可以用来识别价涨量缩的市场（大户主导的市场）。
    # 如果NVI上穿NVI_MA，则产生买入信号；
    # 如果NVI下穿NVI_MA，则产生卖出信号。

    nvi_inc = np.where(df['volume'] < df['volume'].shift(1),
                       1 + (df['close'] - df['close'].shift(1)) / (1e-9 + df['close']), 1)
    nvi_inc[0] = 100
    nvi = pd.Series(nvi_inc).cumprod()
    nvi_ma = nvi.rolling(n, min_periods=1).mean()

    signal = nvi - nvi_ma
    df[factor_name] = scale_01(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
