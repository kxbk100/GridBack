#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from utils.diff import add_diff, eps


def signal(*args):
    # ZhangDieFuAllHour
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]
    
    zhangdiefu_hour_list = [2, 3, 5]
    #  --- 涨跌幅_all_hour ---
    for m in zhangdiefu_hour_list:
        df[f'涨跌幅_bh_{m}'] = df['close'].pct_change(m)
        if m == zhangdiefu_hour_list[0]:
            df[f'涨跌幅_all_hour'] = df[f'涨跌幅_bh_{m}']
        else:
            df[f'涨跌幅_all_hour'] = df[f'涨跌幅_all_hour'] + df[f'涨跌幅_bh_{m}']
        del df[f'涨跌幅_bh_{m}']

    df[factor_name] = df[f'涨跌幅_all_hour'] / len(zhangdiefu_hour_list)

    del df[f'涨跌幅_all_hour']
    
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
