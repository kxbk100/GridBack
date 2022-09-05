"""
花式网格船队 第2期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
import os
import pandas as pd

# =====文件目录
_ = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径
root_path = os.path.abspath(os.path.join(_, '../'))  # 返回根目录文件夹

# ===== 网格回测参数
ini_cap = 10000  # 起始投入
c_rate = 2 / 10000  # 手续费  还可以更低
c_rate_taker = 4 / 10000  # 市价单 手续费
leverage = 3  # 杠杆比例
grid_count = 90  # 网格数目
stop_limit = 0.01  # # 超过最高或最低价一定比例，就强制全部平仓。

# 网格策略回测参数
period = '12H'  # 多久调仓一次，不建议超过24H
offset = 3  # offset参数，如果想回测1天，记得填24H，要不然这个参数会有错误

# 选币因子
factors = {'涨跌幅': True, '振幅': False}
# factors = {'Sgcz_2': True}
strategy_start = '2021-01-01'  # 回测开始时间
strategy_end = '2022-08-20'  # 回测结束时间
grid_price_limit = (0.5, 0.5)  # 最高最低价为指定价格的多少百分比
stop_loss = 0.05  # 网格止损比例。达到固定的亏损比例就止损
stop_profit = 0.02  # 网格止盈比例。达到固定的亏损比例就止损
filters = ['COCOS', 'BTCST', 'DREP', 'SUN', 'BTCDOM', 'DEFI']  # 需要过滤的币种

# 扩散指标阈值
diffusion_limit = (0.1, 0.9)  # 扩散指标在 0.1 - 0.9，之间选币。不在这个范围内，认为市场处于极端情况（暴涨/暴跌），策略空仓

# 主动止盈止损的因子计算周期
active_stop_period = '1H'
# 主动止盈止损的因子路径
active_stop_file_path = root_path + '/data/数据整理/主动止盈止损数据/'
if not os.path.exists(active_stop_file_path):
    os.mkdir(active_stop_file_path)

# 永续合约历史1分钟数据，下载链接：https://www.quantclass.cn/data/coin/coin-binance-swap-candle-csv
candle_path = '/Users/yanjichao/develop/quant/history_candle_data/binance/swap/swap_1m_pkl'
file_type = 'pkl'

# 合约的最小下单量
min_amount_df = pd.read_csv(root_path + '/data/原始数据/最小下单量.csv', encoding='gbk')
min_amount = {}
for i in min_amount_df.index:
    min_amount[min_amount_df.at[i, '合约']] = min_amount_df.at[i, '最小下单量']


def set_value(new_offset):
    global offset
    offset = new_offset
