"""
花式网格船队 第1期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
from program.Function import *


factor_str_info = factor_info_to_str(factors)
evaluate_df = pd.read_csv(root_path + '/data/回测结果/回测指标_%s.csv' % factor_str_info, encoding='gbk')
evaluate_df.rename(columns={'Unnamed: 0': '回测', '0': '指标'}, inplace=True)

equity_df = pd.read_csv(root_path + '/data/回测结果/回测评价_%s.csv' % factor_str_info, encoding='gbk')
equity_df = equity_df[['candle_begin_time', 'symbol', '当周期涨跌幅']]

pro_max = equity_df.sort_values('当周期涨跌幅', ascending=False).head(5)
pro_min = equity_df.sort_values('当周期涨跌幅', ascending=True).head(5)

pro_max['当周期涨跌幅'] = pro_max['当周期涨跌幅'].apply(lambda x: str(round(100 * x, 2)) + '%')
pro_min['当周期涨跌幅'] = pro_min['当周期涨跌幅'].apply(lambda x: str(round(100 * x, 2)) + '%')

# 低版本的pandas，不支持 index 参数
# 安装高版本 pandas 命令 ： pip install pandas==1.3.5
tx_evaluate = evaluate_df.to_markdown(index=False)
tx_evaluate = tx_evaluate.replace(':00:00', '点')

tx_pro_max = pro_max.to_markdown(index=False)
tx_pro_min = pro_min.to_markdown(index=False)

with open(root_path + '/program/发帖脚本/样本模板.txt', 'r', encoding='utf8') as file:
    bbs_post = file.read()
    bbs_post = bbs_post % (tx_evaluate, tx_pro_max, tx_pro_min)
    print(bbs_post)
