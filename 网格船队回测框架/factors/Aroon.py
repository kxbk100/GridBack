#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np
import talib
from utils.diff import add_diff

# =====函数  zscore归一化
def scale_zscore(_s, _n):
    _s = (pd.Series(_s) - pd.Series(_s).rolling(_n, min_periods=1).mean()
          ) / pd.Series(_s).rolling(_n, min_periods=1).std()
    return pd.Series(_s)

def signal(*args):
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # ******************** Aroon ********************
    # AroonUp = (N - HIGH_LEN) / N * 100
    # AroonDown = (N - LOW_LEN) / N * 100
    # AroonOs = AroonUp - AroonDown
    # 其中 HIGH_LEN，LOW_LEN 分别为过去N天最高/最低价距离当前日的天数
    # AroonUp、AroonDown指标分别为考虑的时间段内最高价、最低价出现时间与当前时间的距离占时间段长度的百分比。
    # 如果价格当天创新高，则AroonUp等于100；创新低，则AroonDown等于100。Aroon指标为两者之差，
    # 变化范围为-100到100。Aroon指标大于0表示股价呈上升趋势，Aroon指标小于0表示股价呈下降趋势。
    # 距离0点越远则趋势越强。我们这里以20/-20为阈值构造交易信号。如果AroonOs上穿20/下穿-20则产生买入/卖出信号。

    # 求列的 rolling 窗口内的最大值对于的 index
    high_len = df['high'].rolling(n, min_periods=1).apply(lambda x: pd.Series(x).idxmax())
    # 当前日距离过去N天最高价的天数
    high_len = df.index - high_len
    aroon_up = 100 * (n - high_len) / n

    low_len = df['low'].rolling(n, min_periods=1).apply(lambda x: pd.Series(x).idxmin())
    low_len = df.index - low_len
    aroon_down = 100 * (n - low_len) / n

    signal = aroon_up - aroon_down
    df[factor_name] = scale_zscore(signal, n)

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

