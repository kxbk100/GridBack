"""
花式网格船队 第2期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
import pandas as pd
import numpy as np
import datetime
from Active_stop import calc_stop_signal, stop_loss_or_profit


def import_benchmark_data(path, rul_type, start, end):
    """
    导入基准数据
    :param end: 回测结束时间
    :param start: 回测开始时间
    :param path:币种路径
    :param rul_type:时间频率
    :return:
    """
    # 导入业绩比较基准 （币种）
    if path[-4:] == '.csv':
        benchmark_coin = pd.read_csv(path, encoding='gbk', parse_dates=['candle_begin_time'], skiprows=1)
    else:
        benchmark_coin = pd.read_pickle(path)
    # 生成时间序列
    benchmark = pd.DataFrame(pd.date_range(start=start, end=end, freq=rul_type))
    benchmark.rename(columns={0: 'candle_begin_time'}, inplace=True)
    # 将业绩比较基准往时间序列上合并
    benchmark = pd.merge(left=benchmark, right=benchmark_coin, on='candle_begin_time', how='left')
    # 填充空值
    benchmark['close'].fillna(method='ffill', inplace=True)
    benchmark['open'].fillna(value=benchmark['close'], inplace=True)

    benchmark['基准涨跌幅'] = benchmark['close'].pct_change()
    benchmark['基准涨跌幅'].fillna(value=benchmark['close'] / benchmark['open'] - 1, inplace=True)
    benchmark.rename(columns={'close': '基准收盘价'}, inplace=True)
    # 只保留需要的数据
    benchmark = benchmark[['candle_begin_time', '基准涨跌幅', '基准收盘价']]
    benchmark.reset_index(inplace=True, drop=True)

    return benchmark


def merge_with_benchmark_for_grid(df, benchmark):
    """
    防止数字货币有停牌，将数据与基准数据合并
    :param df: 币种数据
    :param benchmark: 基准数据
    :return:
    """

    # 记录币种最后一个交易日
    coin_last_date = df['candle_begin_time'].iloc[-1]
    # ===将现货数据和BTC现货数据合并，结果已经排序
    df = pd.merge(left=df, right=benchmark, on='candle_begin_time', how='right', sort=True, indicator=True)
    # ===对开、高、收、低、前收盘价价格进行补全处理
    # 用前一天的收盘价，补全收盘价的空值
    df['close'].fillna(method='ffill', inplace=True)
    # 用收盘价补全开盘价、最高价、最低价的空值
    df['open'].fillna(value=df['close'], inplace=True)
    df['high'].fillna(value=df['close'], inplace=True)
    df['low'].fillna(value=df['close'], inplace=True)
    # 资金费率用0填充
    df['fundingRate'].fillna(value=0, inplace=True)

    # ===用前一天的数据，补全其余空值
    df.fillna(method='ffill', inplace=True)
    # 剔除币种上市前的数据
    df.dropna(subset=['symbol'], inplace=True)

    # 删除币种退市后的交易
    df = df[df['candle_begin_time'] <= coin_last_date]

    # ===判断计算当天是否交易
    df['是否交易'] = 1
    df.loc[df['_merge'] == 'right_only', '是否交易'] = 0
    del df['_merge']

    df.reset_index(drop=True, inplace=True)

    return df


# 构建等差网格
def grid_order_info(cap, leverage, low, high, grid_num, limit, min_amount, max_rate=0.95):
    """
    :param cap: 投入资金数量
    :param leverage: 杠杆倍数
    :param low: 最低价
    :param high: 最高价
    :param grid_num: 网格数量
    :param limit: 破网止损比例
    :param min_amount: 该币种最小下单量
    :param max_rate: 币安网格的资金系数，目前是0.95
    :return:
    """

    # ===计算网格：每个格子的价格序列
    # 等比网格规律：网格最低价 x q^n = 最高价，q为等比比例(q>1)，n为网格数目count
    # 所以q = (最高价 / 最低价) ** (1 / n)
    q = (high / low) ** (1 / grid_num)
    price_array = []
    for i in range(0, grid_num + 1):
        price_array.append(low * (q ** i))
    price_array = np.array(price_array).round(8)  # 将网格从list转变为array格式，并且保留8位小数

    # ===计算每个格子的下单数量
    # (p1 * num + p2 * num + p3 * num + ...) = 投入资金 * 杠杆数量 * 资金系数（目前币安市95%）
    order_num = cap * leverage * max_rate / price_array.sum()

    # 根据合约最小下单量调整下单币数
    order_num = order_num - order_num % min_amount
    if order_num <= 0:  # 防止下单量为0
        print('保证金数量太低，无法建立网格')
        exit()

    # ===计算止损价格
    stop_low = low * (1 - limit)
    stop_high = high * (1 + limit)

    # ===返回结果
    grid_info = {
        '价格序列': price_array,
        '每笔数量': order_num,
        '终止最低价': stop_low,
        '终止最高价': stop_high,
    }

    return grid_info


def trans_candle_to_tick(df, grid_info):
    """
    将分钟级别的K线数据转为逐笔数据，这是个近似的转换。
    :param df: 分钟数据
    :param grid_info: 网格信息
    :return:
    """
    data = df[['candle_begin_time', 'open', 'high', 'low', 'close']].copy()

    # ===判断K线是上涨模式还是下跌模式,分钟数据去近似K线数据
    # 上涨K线模式：开->低->高->收  下跌K线模式：开->高->低->收。
    # 沿着波动最小的路径走。
    # 注意：这么做其实不准确，是没有逐笔数据的妥协处理，会有微小误差
    data.loc[data['close'] >= data['open'], 'mode'] = 1  # 上涨模式
    data.loc[data['close'] < data['open'], 'mode'] = -1  # 下跌模式

    # 标记价格顺序
    data['p1'] = data['open']
    data.loc[data['mode'] == 1, 'p2'] = data['low']
    data.loc[data['mode'] == -1, 'p2'] = data['high']
    data.loc[data['mode'] == 1, 'p3'] = data['high']
    data.loc[data['mode'] == -1, 'p3'] = data['low']
    data['p4'] = data['close']

    # ===将k线数据转为逐笔数据
    _dict = {'p1': 0, 'p2': 15, 'p3': 30, 'p4': 45}
    ticks = []
    for key in _dict.keys():
        _ = data[['candle_begin_time', key]]
        _['candle_begin_time'] = _['candle_begin_time'] + datetime.timedelta(seconds=_dict[key])
        _.rename(columns={key: 'tick_price'}, inplace=True)
        ticks.append(_)
    tick_df = pd.concat(ticks, ignore_index=True)
    tick_df.sort_values(by='candle_begin_time', inplace=True)
    tick_df.reset_index(drop=True, inplace=True)

    # ===标记是否破网，并删除破网之后的数据
    tick_df['stop'] = np.nan
    # 理论上是否破网取决于标记价格，此处直接用价格代替
    tick_df.loc[tick_df['tick_price'] > grid_info['终止最高价'], 'stop'] = 1
    tick_df.loc[tick_df['tick_price'] < grid_info['终止最低价'], 'stop'] = 1
    # 删除第一次破网之后的数据
    stop = tick_df[tick_df['stop'] == 1]
    if not stop.empty:
        inx = stop.index[0]
        tick_df = tick_df[:inx + 1]  # 只取未破网的数据
    del tick_df['stop']

    return tick_df


def grid_touch_info(df, grid_info):
    """
    根据tick的数据生成触网的信息
    :param df: tick数据
    :param grid_info: 网格信息
    :return:
    """
    touch_df = df.copy()
    price_array = grid_info['价格序列']

    # ===== 遍历价格序列，计算触网条件
    # 触网条件1 ：上一个tick_price < 网格价格 <= 当前tick_price
    # 触网条件2 ：上一个tick_price > 网格价格 >= 当前tick_price
    for p in price_array:
        touch_df[p] = ''  # 将该列设置为字符串
        touch_df.loc[(touch_df['tick_price'].shift() < p) & (p <= touch_df['tick_price']), p] = '%s_' % p
        touch_df.loc[(touch_df['tick_price'].shift() > p) & (p >= touch_df['tick_price']), p] = '%s_' % p

    # 触网信息汇总
    touch_df['touch'] = touch_df[list(price_array)].sum(axis=1, skipna=True)

    # 将触网信息由字符串转换为list
    def wash_touch(x):
        if x == '':
            return np.nan
        else:
            t_list = x.split('_')[:-1]
            t_list = [float(t) for t in t_list]
            return t_list

    touch_df['touch'] = touch_df['touch'].apply(wash_touch)
    touch_df.drop(columns=list(price_array), axis=1, inplace=True)  # 删除不必要的列，工具人的生命结束了

    # 只保留触网的行，并计算触网次数
    touch_df['last_tick'] = touch_df['tick_price'].shift()  # 保留上一次的tick数据
    touch_df = touch_df[touch_df['touch'].notnull()]  # 去除没有触网的行
    touch_df.reset_index(drop=True, inplace=True)
    touch_df['touch_times'] = touch_df['touch'].apply(lambda x: len(x))  # 计算触网了多少次

    # ====处理多次触网价格顺序问题
    # tick_price上涨,多次触网的序列从小到大排列。（本来就这么排列的，不用处理）
    # tick_price下跌,多次触网的序列从大到小排列。
    con = touch_df['tick_price'] < touch_df['last_tick']
    con &= touch_df['touch_times'] > 1
    touch_df.loc[con, 'touch'] = touch_df['touch'].apply(lambda x: sorted(x, reverse=True))

    # 只保留必要的数据
    touch_df = touch_df[['candle_begin_time', 'tick_price', 'touch', 'touch_times']]

    # 如果没有触网
    if touch_df.empty:
        print('未发生触网')
        # exit()

    return touch_df


def get_trade_info(touch_df, open_price, grid_info):
    """
    从触网数据获取交易的信息
    :param touch_df: 触网数据
    :param open_price: 网格的起始价格
    :param grid_info: 网格信息
    :return:
    """
    # ====将触网信息展开，成为交易信息
    trade_df = pd.DataFrame()
    touch_df['time_list'] = touch_df.apply(lambda rows: [rows['candle_begin_time']] * rows['touch_times'], axis=1)
    trade_df['candle_begin_time'] = touch_df['time_list'].sum()
    trade_df['touch'] = touch_df['touch'].sum()

    # ===== 交易信息清理
    # 清理条件1：当价格在某个网格附近波动时，会多次触网，但只有第一次的触网会真实下单，所以要删除之后无效的触网信息
    con = trade_df['touch'] == trade_df['touch'].shift()
    trade_df = trade_df[~con]
    # （可以无视）清理条件2：如果第一次触网的价格是离现价最近的价格，那么不会挂单
    price_array = grid_info['价格序列']
    diff_array = abs(price_array - open_price)
    closest_index = np.argmin(diff_array)
    closest_grid_price = price_array[closest_index]
    if trade_df['touch'].iloc[0] == closest_grid_price:
        trade_df = trade_df[1:]
    # 重置索引
    trade_df.reset_index(drop=True, inplace=True)
    if trade_df.empty:
        return pd.DataFrame(), 0.0

    # ===== 整理交易信息
    # 根据上一次的触网价格生成挂单方向
    trade_df['last_touch'] = trade_df['touch'].shift()
    trade_df['last_touch'].fillna(value=open_price, inplace=True)  # 第1次触网价格的上次触网价格就是第一根K线的价格
    # 下单
    trade_df.loc[trade_df['last_touch'] > trade_df['touch'], 'order_dir'] = 1  # 从上往下触网，下买单
    trade_df.loc[trade_df['last_touch'] < trade_df['touch'], 'order_dir'] = -1  # 从下往上触网，下卖单
    trade_df['order_num'] = grid_info['每笔数量']  # 每次下单同样的币种数目
    # 只取必要的列
    trade_df = trade_df[['candle_begin_time', 'last_touch', 'touch', 'order_dir', 'order_num']]

    # 简单的估算一下最终盈利（未考虑爆仓、并且没有计算手续费）
    end_price = trade_df['touch'].iloc[-1]
    trade_df['profit'] = (end_price - trade_df['touch']) * trade_df['order_num'] * trade_df['order_dir']
    profit = trade_df['profit'].sum()
    del trade_df['profit']

    return trade_df, profit


def cal_equity_curve_for_grid(candle_df, trade_df, fee, cap, margin_rate=0.05, stop_loss=0.05, stop_profit=0.02):
    """
    计算网格的资金曲线
    :param candle_df: 分钟数据
    :param trade_df: 交易数据
    :param fee: 手续费率
    :param cap: 初始投入的资金
    :param margin_rate: 维持保证金率，净值低于这个比例会爆仓
    :param stop_loss: 止损比例
    :param stop_profit: 止盈比例
    :return:
    """
    trade_data = trade_df.copy()
    candle_data = candle_df.copy()

    # ===== 计算下单手续费
    trade_data['fee'] = trade_data['order_num'] * trade_data['touch'] * fee  # 挂单手续费低，并且无滑点

    # ===== 计算已实现盈亏
    trade_data['net_dir'] = trade_data['order_dir'].expanding().sum()  # 计算净头寸
    # 净头寸绝对值减小的地方，即为发生平仓的地方。
    con = (abs(trade_data['net_dir']) - abs(trade_data['net_dir'].shift())) < 0
    # 平仓利润 = 网格间隙 x 下单数量。平仓时网格的间隙：必定是相差一格（见ppt第一张图），即为上一次网格经过的地方。
    trade_data['grid_gap'] = abs(trade_data['last_touch'] - trade_data['touch'])
    trade_data.loc[con, 'real_profit'] = trade_data['grid_gap'] * trade_data['order_num']
    del trade_data['grid_gap'], trade_data['last_touch']

    # ====计算未实现盈亏
    trade_data['hold_num'] = trade_data['net_dir'] * trade_data['order_num']  # 持币数，可能为负（做空时）
    # 根据原理计算持仓均价：净头寸相同的地方，开仓价格一定相同；净头寸相同的地方，持仓均价一定相同。
    price_df = trade_data[['touch', 'net_dir']].drop_duplicates(subset=['net_dir']).copy()
    # 将数据拆分为净头寸>0和净头寸<0的部分
    positive_df = price_df[price_df['net_dir'] > 0].sort_values('net_dir', ascending=True)
    negative_df = price_df[price_df['net_dir'] < 0].sort_values('net_dir', ascending=False)
    # 计算均价
    if not positive_df.empty:
        positive_df['avg_price'] = positive_df['touch'].expanding().mean()
    if not negative_df.empty:
        negative_df['avg_price'] = negative_df['touch'].expanding().mean()
    # 合并数据
    price_df = pd.concat([positive_df, negative_df], ignore_index=True)
    # 合并数据计算均价
    trade_data = pd.merge(left=trade_data, right=price_df[['net_dir', 'avg_price']], on='net_dir', how='left')
    # 净头寸为0的地方，均价也为0
    trade_data['avg_price'].fillna(value=0, inplace=True)
    del trade_data['touch'], trade_data['order_dir'], trade_data['order_num']
    # end_trade_time = trade_data['candle_begin_time'].iloc[-1]

    # 合并K先数据 & 交易数据
    # 合并数据
    # candle_data = candle_data[candle_data['candle_begin_time'] <= end_trade_time]
    df = pd.merge(left=candle_data, right=trade_data, on=['candle_begin_time'], how='outer', sort=True)  # 有+15s、30s、45s，所以用outer
    del df['high'], df['low'], df['是否交易']

    # 填充空数据
    for col in ['close', 'open', 'net_dir', 'hold_num', 'avg_price', '基准收盘价', 'symbol']:
        df[col].fillna(method='ffill', inplace=True)
    for col in ['fee', 'real_profit', 'fundingRate', '基准涨跌幅']:
        df[col].fillna(value=0.0, inplace=True)

    # 计算未实现盈亏
    df['unreal_profit'] = df['hold_num'] * (df['close'] - df['avg_price'])

    # 计算资金费率：+代表需要给出去的钱，-代表能收回钱
    df['fr_fee'] = df['hold_num'] * df['open'] * df['fundingRate']  # 用open代替会有微小的误差，可以忽略

    # 计算累计值
    df['fee'] = df['fee'].expanding().sum()
    df['fr_fee'] = df['fr_fee'].expanding().sum()
    df['real_profit'] = df['real_profit'].expanding().sum()
    # 计算累计利润、资金曲线
    df['profit'] = df['real_profit'] - df['fr_fee'] - df['fee'] + df['unreal_profit']
    df['net_value'] = (df['profit'] + cap) / cap
    df['net_value'].fillna(value=1, inplace=True)

    # 计算止盈止损
    df = stop_loss_or_profit(df, stop_loss, cap, stop_profit)

    # 计算爆仓
    df['是否爆仓'] = np.nan
    df.loc[df['net_value'] < margin_rate, '是否爆仓'] = 1
    df['是否爆仓'].fillna(method='ffill', inplace=True)
    df.loc[df['是否爆仓'] == 1, 'net_value'] = 0.0
    if 1 in df['是否爆仓'].to_list():
        print('\n菜鸡，叫你高杠杆！！！发生爆仓，裤衩都没啦！！！')

    # 计算基准
    df['基准净值'] = df['基准收盘价'] / df['基准收盘价'].iloc[0]

    return df


def evaluate_investment_for_grid(pos_data, date='交易日期', nv_col='net_value'):
    """
    回测评价函数
    :param pos_data:资金曲线
    :param nv_col:资金曲线列名
    :param date:交易日期
    :return:
    """
    temp = pos_data.copy()
    # ===新建一个dataframe保存回测指标
    results = pd.DataFrame()

    # 将数字转为百分数
    def num_to_pct(value):
        return '%.2f%%' % (value * 100)

    # ===计算累积净值
    results.loc[0, '累积净值'] = round(temp[nv_col].iloc[-1], 2)

    # ===计算年化收益
    annual_return = (temp[nv_col].iloc[-1]) ** (
            '1 days 00:00:00' / (temp[date].iloc[-1] - temp[date].iloc[0]) * 365) - 1
    results.loc[0, '年化收益'] = num_to_pct(annual_return)

    # ===计算最大回撤，最大回撤的含义：《如何通过3行代码计算最大回撤》https://mp.weixin.qq.com/s/Dwt4lkKR_PEnWRprLlvPVw
    # 计算当日之前的资金曲线的最高点
    temp['max2here'] = temp[nv_col].expanding().max()
    # 计算到历史最高值到当日的跌幅，drowdwon
    temp['dd2here'] = temp[nv_col] / temp['max2here'] - 1
    # 计算最大回撤，以及最大回撤结束时间
    end_date, max_draw_down = tuple(temp.sort_values(by=['dd2here']).iloc[0][[date, 'dd2here']])
    # 计算最大回撤开始时间
    start_date = temp[temp[date] <= end_date].sort_values(by=nv_col, ascending=False).iloc[0][
        date]
    # 将无关的变量删除
    temp.drop(['max2here', 'dd2here'], axis=1, inplace=True)
    results.loc[0, '最大回撤'] = num_to_pct(max_draw_down)
    results.loc[0, '最大回撤开始时间'] = str(start_date)
    results.loc[0, '最大回撤结束时间'] = str(end_date)

    # ===年化收益/回撤比：我个人比较关注的一个指标
    results.loc[0, '年化收益/回撤比'] = round(annual_return / abs(max_draw_down), 2)

    return results.T


def grid_back_test(infos):
    print('%s   %s    最高价：%.8f  最低价：%.8f' % (infos['start'], infos['symbol'], infos['grid_high'], infos['grid_low']))

    # =====读取数据
    benchmark = import_benchmark_data(infos['bench_path'], start=infos['start'], end=infos['end'], rul_type='60s')
    # 读取币种数据
    if infos['coin_path'][-4:] == '.csv':
        df = pd.read_csv(infos['coin_path'], encoding='gbk', parse_dates=['candle_begin_time'], skiprows=1)
    else:
        df = pd.read_pickle(infos['coin_path'])
    # 减少获取的数据量，可以加快回测速度
    df = df[df.candle_begin_time.between(infos['start'] - datetime.timedelta(days=1),
                                         infos['end'] + datetime.timedelta(days=1))].copy()

    # 将币种数据和基准合并，填充空值
    df = merge_with_benchmark_for_grid(df, benchmark)
    if df.empty:
        return pd.DataFrame()

    # 根据输入参数，生成网格信息
    grid_info = grid_order_info(cap=infos['cap'], leverage=infos['leverage'], low=infos['grid_low'],
                                high=infos['grid_high'], grid_num=infos['grid_num'], limit=infos['limit'],
                                min_amount=infos['min_amount'])

    # =====将分钟数据转为tick数据
    tick_df = trans_candle_to_tick(df, grid_info)  # 如果直接有tick数据的话，可以直接用，无缝衔接

    # 计算主动止盈止损信号
    df = calc_stop_signal(df, infos)

    # =====根据网格信息生成触网信息
    touch_df = grid_touch_info(df=tick_df, grid_info=grid_info)
    if touch_df.empty:
        return pd.DataFrame()

    # =====根据触网信息，生成交易信息，估算大致盈利
    trade_df, profit = get_trade_info(touch_df, open_price=df['open'].iloc[0], grid_info=grid_info)
    if trade_df.empty:
        return pd.DataFrame()
    # print('预估利润：', profit)

    # 计算资金曲线
    df = df[df['candle_begin_time'] <= tick_df['candle_begin_time'].iloc[-1]]
    df = cal_equity_curve_for_grid(candle_df=df, trade_df=trade_df, fee=infos['fee'], cap=infos['cap'],
                                   stop_loss=infos['stop_loss'], stop_profit=infos['stop_profit'])

    # 计算每日净值变化
    df['nv_change'] = df['net_value'].pct_change()
    df['nv_change'].fillna(value=df['net_value'] - 1, inplace=True)

    # 只输出必要的列
    df = df[['candle_begin_time', 'symbol', '基准涨跌幅', '基准净值', 'net_value', 'nv_change', '是否爆仓']]
    return df
