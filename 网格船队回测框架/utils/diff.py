#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy  as np

from fracdiff import fdiff
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)

eps = 1e-8


def add_diff(_df, _d_num, _name, _window=10):
    if len(_df) >= 12:  # 数据行数大于等于12才进行差分操作
        _diff_ar = fdiff(_df[_name], n=_d_num, window=_window, mode="valid")  # 列差分，不使用未来数据
        _paddings = len(_df) - len(_diff_ar)  # 差分后数据长度变短，需要在前面填充多少数据
        _diff = np.nan_to_num(np.concatenate((np.full(_paddings, 0), _diff_ar)), nan=0)  # 将所有nan替换为0
        _df[_name] = _diff  # 将差分数据记录到 DataFrame
    else:
        _df[_name] = np.nan  # 数据行数不足12的填充为空数据

    return _df


