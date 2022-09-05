"""
花式网格船队 第2期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
import warnings
from multiprocessing import cpu_count, Pool
from Function import *
from Grid_function import *
from Fancy_grid_function import *

warnings.filterwarnings('ignore')

if __name__ == '__main__':
    # 将字典转成字符串名称，便于保存回测文件时使用
    factor_str_info = factor_info_to_str(factors)

    # 读取选中币种的数据
    factor_data = pd.read_pickle(root_path + f'/data/数据整理/all_coin_factor_data.pkl')
    # 选择时间段
    factor_data = factor_data[factor_data['time'] >= pd.to_datetime(strategy_start)]
    factor_data = factor_data[factor_data['time'] <= pd.to_datetime(strategy_end)]

    # 选择币种
    factor_data = select_grid_coin(factor_data, factors)
    # 保存选币信息，供策略评价时使用（3_策略评价详情.py）
    factor_data.to_csv(root_path + '/data/回测结果/选币结果_%s.csv' % factor_str_info, encoding='gbk', index=False)

    # 计算网格交易的信息
    # 计算时间间隔
    span = pd.to_timedelta(period)
    # 下一分钟开仓
    factor_data['start'] = factor_data['time'] + datetime.timedelta(minutes=1)
    factor_data['end'] = factor_data['time'] + span

    # 生成每个周期的网格的下单信息
    info_list = create_order_info(factor_data)

    # 针对每个周期，独立计算该周期网格的资金曲线。关键函数：grid_back_test
    start_time = datetime.datetime.now()
    # 并行或串行读取数据
    multiply_process = True
    if multiply_process:
        # 开始并行
        with Pool(max(cpu_count() - 1, 1)) as pool:
            df_list = pool.map(grid_back_test, info_list)
    else:
        df_list = []
        for i in info_list:
            data = grid_back_test(i)
            df_list.append(data)

    # 合并资金曲线
    all_back_test = pd.concat(df_list, ignore_index=True)
    all_back_test.sort_values(by='candle_begin_time', inplace=True)
    all_back_test.reset_index(drop=True, inplace=True)
    all_back_test['nv_change'].fillna(value=0, inplace=True)
    # 计算合并之后的净值，处理爆仓
    all_back_test['strategy_nv'] = (all_back_test['nv_change'] + 1).cumprod()
    all_back_test['是否爆仓'].fillna(method='ffill', inplace=True)
    all_back_test.loc[all_back_test['是否爆仓'] == 1, 'strategy_nv'] = 0
    all_back_test.reset_index(inplace=True)

    res = evaluate_investment_for_grid(all_back_test, date='candle_begin_time', nv_col='strategy_nv')
    print(res)

    col_dict = {'网格净值': 'strategy_nv'}
    factor_str_info = factor_info_to_str(factors)
    pic_title = 'factor:%s_lvg:%s_num:%s_nv:%s_pro:%s_risk:%s' % (factor_str_info, leverage, grid_count,
                                                                  res.at['累积净值', 0], res.at['年化收益', 0],
                                                                  res.at['最大回撤', 0])
    draw_equity_curve_plotly(all_back_test, data_dict=col_dict, date_col='candle_begin_time', title=pic_title)
    # draw_equity_curve_mat(all_back_test, data_dict=col_dict, date_col='candle_begin_time', title=pic_title)

    all_back_test = all_back_test[['candle_begin_time', 'symbol', 'strategy_nv', 'nv_change']]
    all_back_test.to_csv(root_path + '/data/回测结果/%s.csv' % factor_str_info, encoding='gbk', index=False)
