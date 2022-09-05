"""
花式网格船队 第2期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
import os.path

from Config import *
from factors.index import allFactors


def cal_factor(df):
    """
    计算单个币种的因子值
    :param df:
    :return:
    """
    # 每日涨跌幅
    df['涨跌幅'] = df['close'].pct_change()
    df['涨跌幅'].fillna(value=df['close'] / df['open'] - 1, inplace=True)

    df['振幅'] = (df['high'] - df['low']) / df['open']

    # 判断币种是上涨还是下跌
    df['上涨'] = 0
    df['下跌'] = 0
    df.loc[df['涨跌幅'] > 0, '上涨'] = 1
    df.loc[df['涨跌幅'] <= 0, '下跌'] = 1

    # 根据指定的参数计算一些技术指标
    # for n in [2, 3, 5, 8, 13]:
    #     df['ma_%s' % n] = df['close'].rolling(n).mean()
    #     df['bias_%s' % n] = df['close'] / df['ma_%s' % n] - 1
    # for n in [2]:
    #     for factor in factors:
    #         # if check_contain_chinese(factor):
    #         #     print('中文')
    #         # else:
    #         _symbol = factor[:-2]
    #         allFactors[_symbol](df, n, 0, _symbol + '_%s' % n)
    #         print('计算因子-', _symbol + '_%s' % n)

    # 判断价格是否在DC通道内
    df['dc_dn'] = df['low'].rolling(20, min_periods=1).min()
    df['dc'] = 0
    df.loc[df['close'] > df['dc_dn'], 'dc'] = 1

    return df


def cal_cross_factor(all_coin_data):
    """
    计算截面的因子数据
    :param all_coin_data:
    :return:
    """
    all_coin_data['上涨数量'] = all_coin_data.groupby('time')['上涨'].transform('sum')
    all_coin_data['下跌数量'] = all_coin_data.groupby('time')['下跌'].transform('sum')
    all_coin_data['上涨比例'] = all_coin_data['上涨数量'] / (all_coin_data['上涨数量'] + all_coin_data['下跌数量'])
    return all_coin_data


def select_grid_coin(data, factor_info):
    """
    选择网格币种，可以加入择时的方法
    :param data:
    :param factor_info:
    :return:
    """
    # 删除选币因子为空的数据
    data.dropna(subset=list(factor_info.keys()), inplace=True)

    # DC择时：收盘价在通道内
    con3 = data['dc'] == 1
    data = data[con3]


    # 排序
    rank_col = []
    for factor in factor_info:
        data['rank_%s' % factor] = data.groupby('time')[factor].rank(method='first', ascending=factor_info[factor])
        rank_col.append('rank_%s' % factor)

    # 排序相加
    data['rank_sum'] = data[rank_col].sum(axis=1)
    data['rank'] = data.groupby('time')['rank_sum'].rank(method='first', ascending=True)
    # 选币
    data = data[data['rank'] == 1]  # 根据配置筛选选币数量

    # （大盘择时）筛选条件：10%<上涨比例<90%，不在这个范围内的时候空仓
    # con1 = data['上涨比例'] > diffusion_limit[0]
    # con2 = data['上涨比例'] < diffusion_limit[1]
    # data = data[con1 & con2]

    data.sort_values(by='time', inplace=True)

    return data


def create_order_info(factor_data):
    """
    生成下单参数，可以根据因子动态生成，也可以固定。
    :param factor_data:
    :return:
    """
    # 网格的最高价格
    factor_data['grid_high'] = factor_data['close'] * (1 + grid_price_limit[1])
    factor_data['grid_low'] = factor_data['close'] * (1 - grid_price_limit[0])

    # 生产每天网格的下单信息
    info_list = []
    for i in factor_data.index:
        info_dict = {
            'start': factor_data.at[i, 'start'],
            'end': factor_data.at[i, 'end'],
            'symbol': factor_data.at[i, 'symbol'],
            'grid_high': factor_data.at[i, 'grid_high'],
            'grid_low': factor_data.at[i, 'grid_low'],
            'bench_path': os.path.join(candle_path, factor_data.at[i, 'symbol'] + '.%s' % file_type),
            'coin_path': os.path.join(candle_path, factor_data.at[i, 'symbol'] + '.%s' % file_type),
            'cap': ini_cap,
            'leverage': leverage,
            'grid_num': grid_count,
            'limit': stop_limit,
            'min_amount': min_amount[factor_data.at[i, 'symbol']],
            'fee': c_rate,
            'stop_loss': stop_loss,
            'stop_profit': stop_profit
        }
        info_list.append(info_dict)

    return info_list
