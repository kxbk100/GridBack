#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy  as np
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Trrq 指标
    
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['tp'] = (df['high'] + df['low'] + df['close']) / 3
    df['归一成交额'] = df['quote_volume'] / \
        df['quote_volume'].rolling(n, min_periods=1).mean()
    reg_price = ta.LINEARREG(df['tp'], timeperiod=n)
    df['tp_reg涨跌幅'] = reg_price.pct_change(n)
    df['tp_reg涨跌幅除以归一成交额'] = df['tp_reg涨跌幅'] / (eps + df['归一成交额'])
    df[factor_name] = df['tp_reg涨跌幅除以归一成交额'].rolling(n).sum()

    del df['tp'], df['归一成交额'], df['tp_reg涨跌幅'], df['tp_reg涨跌幅除以归一成交额']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df










        
