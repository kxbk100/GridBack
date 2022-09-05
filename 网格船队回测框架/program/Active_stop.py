"""
花式网格船队 第2期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
import datetime
import os
import numpy as np
from Config import c_rate_taker, pd, active_stop_file_path


# 计算主动止盈止损的因子
def calc_active_stop_factor(df):
    """
    计算主动止盈止损的因子
    :param df: 原始币种的1m全量数据，需要全量数据来计算，这样更加准确
    :return:
    """
    # 最终需要保留的列名
    save_cols = ['time', 'symbol', 'open', 'high', 'low', 'close', 'quote_volume']

    # ===案例1：计算放量相关因子
    for n in [2, 3, 5, 8, 13, 21, 34, 55]:
        df[f'last_period_mean_{n}'] = df['quote_volume'].rolling(n).mean()
        save_cols.append(f'last_period_mean_{n}')
    # ======================

    # ===案例2：计算V3相关因子
    # 参考自J神的V3趋势策略：https://bbs.quantclass.cn/thread/1879
    for n in [2, 3, 5, 8, 13, 21, 34, 55]:
        n2 = 35 * n
        df['median'] = df['close'].rolling(window=n2).mean()
        df['std'] = df['close'].rolling(n2, min_periods=1).std(ddof=0)  # ddof代表标准差自由度
        df['z_score'] = abs(df['close'] - df['median']) / df['std']
        df['m'] = df['z_score'].rolling(window=n2).mean()

        df[f'upper_{n}'] = df['median'] + df['std'] * df['m']
        df[f'lower_{n}'] = df['median'] - df['std'] * df['m']

        save_cols.append(f'upper_{n}')
        save_cols.append(f'lower_{n}')

        indicator = f'mtm_mean_{n}'
        save_cols.append(indicator)

        df['mtm'] = df['close'] / df['close'].shift(n) - 1
        df[indicator] = df['mtm'].rolling(window=n, min_periods=1).mean()

        # 基于价格atr，计算波动率因子wd_atr
        df['c1'] = df['high'] - df['low']
        df['c2'] = abs(df['high'] - df['close'].shift(1))
        df['c3'] = abs(df['low'] - df['close'].shift(1))
        df['tr'] = df[['c1', 'c2', 'c3']].max(axis=1)
        df['atr'] = df['tr'].rolling(window=n, min_periods=1).mean()
        df['avg_price'] = df['close'].rolling(window=n, min_periods=1).mean()
        df['wd_atr'] = df['atr'] / df['avg_price']

        # 参考ATR，对MTM指标，计算波动率因子
        df['mtm_l'] = df['low'] / df['low'].shift(n) - 1
        df['mtm_h'] = df['high'] / df['high'].shift(n) - 1
        df['mtm_c'] = df['close'] / df['close'].shift(n) - 1
        df['mtm_c1'] = df['mtm_h'] - df['mtm_l']
        df['mtm_c2'] = abs(df['mtm_h'] - df['mtm_c'].shift(1))
        df['mtm_c3'] = abs(df['mtm_l'] - df['mtm_c'].shift(1))
        df['mtm_tr'] = df[['mtm_c1', 'mtm_c2', 'mtm_c3']].max(axis=1)
        df['mtm_atr'] = df['mtm_tr'].rolling(window=n, min_periods=1).mean()

        # 参考ATR，对MTM mean指标，计算波动率因子
        df['mtm_l_mean'] = df['mtm_l'].rolling(window=n, min_periods=1).mean()
        df['mtm_h_mean'] = df['mtm_h'].rolling(window=n, min_periods=1).mean()
        df['mtm_c_mean'] = df['mtm_c'].rolling(window=n, min_periods=1).mean()
        df['mtm_c1'] = df['mtm_h_mean'] - df['mtm_l_mean']
        df['mtm_c2'] = abs(df['mtm_h_mean'] - df['mtm_c_mean'].shift(1))
        df['mtm_c3'] = abs(df['mtm_l_mean'] - df['mtm_c_mean'].shift(1))
        df['mtm_tr'] = df[['mtm_c1', 'mtm_c2', 'mtm_c3']].max(axis=1)
        df['mtm_atr_mean'] = df['mtm_tr'].rolling(window=n, min_periods=1).mean()

        # mtm_mean指标分别乘以三个波动率因子
        df[indicator] = df[indicator] * df['mtm_atr']
        df[indicator] = df[indicator] * df['mtm_atr_mean']
        df[indicator] = df[indicator] * df['wd_atr']

        # 对新策略因子计算自适应布林
        df['median'] = df[indicator].rolling(window=n).mean()
        df['std'] = df[indicator].rolling(n, min_periods=1).std(ddof=0)  # ddof代表标准差自由度
        df['z_score'] = abs(df[indicator] - df['median']) / df['std']
        df['m'] = df['z_score'].rolling(window=n).min().shift(1)
        df[f'up_{n}'] = df['median'] + df['std'] * df['m']
        df[f'dn_{n}'] = df['median'] - df['std'] * df['m']

        save_cols.append(f'up_{n}')
        save_cols.append(f'dn_{n}')
    # ======================

    # ====增加你想计算的其他因子

    # ======================

    df = df[save_cols]
    df.fillna(method='ffill', inplace=True)
    return df


# 计算主动止盈止损的因子
def calc_stop_signal(df, infos):
    """
    计算主动止盈止损的因子
    :param df: 原始币种的1m全量数据，数据计算有预计算数据，需要全量数据来计算，这样更加准确
    :return:
    """
    # 读取主动止盈止损因子的pkl
    stop_df = pd.read_pickle(os.path.join(active_stop_file_path, infos['symbol'] + '.pkl'))
    # 选取相应时间段，加快回测速度
    stop_df = stop_df[stop_df['time'] >= infos['start'] - datetime.timedelta(days=60)]
    stop_df = stop_df[stop_df['time'] <= infos['end'] + datetime.timedelta(days=1)]

    # 停止平仓信号
    stop_df['stop_signal'] = 0

    # ===案例1：放量止损
    stop_df.loc[stop_df['quote_volume'] > 2 * stop_df['last_period_mean_55'], 'stop_signal'] = 1
    # ==============

    # ===案例2：v3止损
    # condition1 = stop_df['mtm_mean_13'] > stop_df['up_13']  # 当前K线的收盘价 > 上轨
    # condition2 = stop_df['mtm_mean_13'].shift(1) <= stop_df['up_13'].shift(1)  # 之前K线的收盘价 <= 上轨
    # stop_df.loc[condition1 & condition2, 'stop_signal'] = 1
    # condition1 = stop_df['mtm_mean_13'] < stop_df['dn_13']  # 当前K线的收盘价 < 下轨
    # condition2 = stop_df['mtm_mean_13'].shift(1) >= stop_df['dn_13'].shift(1)  # 之前K线的收盘价 >= 下轨
    # stop_df.loc[condition1 & condition2, 'stop_signal'] = 1
    # stop_df['stop_signal'] = stop_df['stop_signal'].shift(1)
    #
    # # 价格超过上轨，只做多
    # condition_long = stop_df['close'] > stop_df['upper_13']
    # # 价格低于下轨，只做空
    # condition_short = stop_df['close'] < stop_df['lower_13']
    # stop_df.loc[condition_long, 'stop_signal'] = 0
    # stop_df.loc[condition_short, 'stop_signal'] = 0
    # ==============

    # ===其他的止盈止损方法，写法类似于择时策略
    # # ==============

    # 整理stop_df
    stop_df = stop_df[['time', 'stop_signal']]
    stop_df = stop_df[stop_df['stop_signal'] == 1]

    # 将止损信号和df合并
    stop_df['time'] += datetime.timedelta(minutes=1)  # stop_df是分钟k线开始的时间，和tick合并需要使用分钟k线结束的时间，所以+1分钟
    df = pd.merge(left=df, right=stop_df, left_on='candle_begin_time', right_on='time', how='left')
    del df['time']
    df['stop_signal'].fillna(method='ffill', inplace=True)

    return df


# 止盈，止损
def stop_loss_or_profit(df, stop_loss, cap, stop_profit):
    # 止盈止损标记
    df['stop'] = np.nan

    # 根据主动止损的信号进行止损
    df.loc[df['stop_signal'] == 1, 'stop'] = 1

    # 固定比例止损
    df.loc[df['net_value'] < 1 - stop_loss, 'stop'] = 1
    # 固定比例止盈
    df.loc[df['net_value'] > 1 + stop_profit, 'stop'] = 1

    # 补全
    df['stop'].fillna(method='ffill', inplace=True)
    df['stop'].fillna(value=0, inplace=True)

    temp = df[df['stop'] == 1]
    if not temp.empty:
        # 只保留止损止盈之前的数据
        inx = temp.index[0]
        df = df[:inx + 1]
        # 取最后一行数据
        row = df.iloc[-1]
        # 计算止损平仓手续费
        fee_rate = abs(row['hold_num']) * row['close'] * c_rate_taker / cap
        df.loc[row.name, 'net_value'] = row['net_value'] - fee_rate

    return df
