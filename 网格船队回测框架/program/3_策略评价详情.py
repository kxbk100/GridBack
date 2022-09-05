"""
花式网格船队 第2期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
from Function import *
import warnings

warnings.filterwarnings('ignore')

# 获取因子名称 即：文件名
factor_str_info = factor_info_to_str(factors)

# =生成基础的周期数据
benchmark = pd.DataFrame(pd.date_range(start=strategy_start, end=strategy_end, freq=period))
benchmark.rename(columns={0: 'candle_begin_time'}, inplace=True)
benchmark.sort_values('candle_begin_time', inplace=True)
benchmark.set_index('candle_begin_time', inplace=True)
benchmark = benchmark.resample(rule=period, base=offset).last()
benchmark.reset_index(inplace=True)
# 如果设置offset，会有个别时间偏移超过范围，手动过滤一下
benchmark = benchmark[
    (benchmark['candle_begin_time'] > strategy_start) & (benchmark['candle_begin_time'] < strategy_end)
]

# =获取分钟资金详情数据，周期转换
df = pd.read_csv(root_path + '/data/回测结果/%s.csv' % factor_str_info, encoding='gbk', parse_dates=['candle_begin_time'])
df.sort_values('candle_begin_time', inplace=True)
df['time'] = df['candle_begin_time']
df.set_index('candle_begin_time', inplace=True)
agg_dict = {
    'symbol': 'last',
}
period_df = df.resample(rule=period, base=offset).agg(agg_dict)
# 计算周期涨跌幅
period_df['nv_change'] = df['nv_change'].resample(period, base=offset).apply(lambda x: (x + 1).prod() - 1)
period_df.reset_index(inplace=True)

# =获取选币数据，周期转换
coin_df = pd.read_csv(root_path + '/data/回测结果/选币结果_%s.csv' % factor_str_info, encoding='gbk', parse_dates=['time'])
coin_df.sort_values('time', inplace=True)
# 选币数据处理的是一分钟数据，经过周期转换，从00开始选取，之后会在整点分钟的时候提前一分钟选出币种，然后在整点下单
# 例子：10分钟周期
# [ 0 1 2 3 4 5 6 7 8 9 ] 这是一个周期，不会到达 10， 我们会在第10分钟下单
# 这里 +1m ， 转换成该币种的实际下单的时间
coin_df['time'] = coin_df['time'] + pd.to_timedelta('1m')
coin_df['candle_begin_time'] = coin_df['time']

# =列出需要合并的列名
merge_cols = ['candle_begin_time', 'symbol'] + list(factors.keys())
# 将计算的资金曲线数据合并到选币数据上
equity_df = pd.merge(left=coin_df[merge_cols], right=period_df, on='candle_begin_time', how='left',
                     suffixes=('', '_r'))
equity_df['nv_change'].fillna(value=0, inplace=True)
equity_df.loc[equity_df['nv_change'] == 0, '备注'] = '未触网'

equity_df['当周期涨跌幅'] = equity_df['nv_change']
equity_df['净值'] = (equity_df['nv_change'] + 1).cumprod()
equity_df['factor'] = factor_str_info
del equity_df['nv_change']
del equity_df['symbol_r']
# print(equity_df)

# =将资金曲线合并到benchmark上，用于填充过滤导致的周期空仓数据
equity_df = pd.merge(left=benchmark, right=equity_df, on='candle_begin_time', how='left')
equity_df['当周期涨跌幅'].fillna(value=0, inplace=True)
equity_df.loc[equity_df['symbol'].isna(), '备注'] = '空仓'
equity_df['净值'] = (equity_df['当周期涨跌幅'] + 1).cumprod()
equity_df['factor'] = factor_str_info
print(equity_df)

# 需要保存的列名
save_cols = ['candle_begin_time', 'factor', 'symbol', '当周期涨跌幅', '净值', '备注'] + list(factors.keys())
equity_df[save_cols].to_csv(root_path + '/data/回测结果/回测评价_%s.csv' % factor_str_info, encoding='gbk', index=False)

# new 策略评价，这里补充了未触网的数据，并且根据周期来进行评价，回撤信息没有分钟级别的细致
res = strategy_evaluate(equity_df, date='candle_begin_time', nv_col='净值')
print(res)
res.to_csv(root_path + '/data/回测结果/回测指标_%s.csv' % factor_str_info, encoding='gbk')
