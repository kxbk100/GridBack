"""
花式网格船队 第2期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
import pandas as pd

from Function import *
from Grid_function import *
import warnings

warnings.filterwarnings('ignore')

# 网格回测参数
symbol = 'LINK-USDT'
info_dict = {
    'start': pd.to_datetime('2022-01-12'),
    'end': pd.to_datetime('2022-01-13'),
    'symbol': symbol,
    'grid_low': 23.9238,  # 网格最低价
    'grid_high': 29.2402,  # 网格最高价
    'limit': stop_limit,  # 超过最高或最低价一定比例，就强制全部平仓。
    'bench_path': os.path.join(candle_path, symbol + '.pkl'),
    'coin_path': os.path.join(candle_path, symbol + '.pkl'),
    'cap': 10000,  # 初始投入资金
    'leverage': 5,  # 杠杆倍数
    'grid_num': 20,  # 网格数量
    'min_amount': min_amount[symbol],
    'fee': 2 / 10000,  # 手续费
    'stop_loss': 1,  # 网格止损比例。达到固定的亏损比例就止损
    'stop_profit': stop_profit,  # 网格止损比例。达到固定的亏损比例就止损
}

# 调用网格回测函数
df = grid_back_test(infos=info_dict)
if df.empty:
    print('回测结果为空，可能未触网。')
    exit()

# 网格评价
res = evaluate_investment_for_grid(df, date='candle_begin_time')
print(res)

col_dict = {'网格净值': 'net_value', '基准净值': '基准净值'}
pic_title = '%s_[%s,%s]_lvg:%s_num:%s_nv:%s_pro:%s_risk:%s' % (symbol, info_dict['grid_low'], info_dict['grid_high'],
                                                               info_dict['leverage'], info_dict['grid_num'],
                                                               res.at['累积净值', 0],
                                                               res.at['年化收益', 0], res.at['最大回撤', 0])
# 绘制资金曲线
# draw_equity_curve_plotly(df, data_dict=col_dict, date_col='candle_begin_time', title=pic_title)
draw_equity_curve_mat(df, data_dict=col_dict, date_col='candle_begin_time', title=pic_title)

print(df.tail(5))
