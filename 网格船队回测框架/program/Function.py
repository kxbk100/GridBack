"""
花式网格船队 第2期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
import itertools
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots

from Config import *

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


def get_code_list_in_one_dir(path, end_with='csv'):
    """
    从指定文件夹下，导入所有数字货币数据
    :param path:
    :param end_with:
    :return:
    """
    symbol_list = []

    # 系统自带函数os.walk，用于遍历文件夹中的所有文件
    for root, dirs, files in os.walk(path):
        if files:  # 当files不为空的时候
            for f in files:
                if f.endswith(end_with):
                    symbol_list.append(os.path.join(root, f))

    return sorted(symbol_list)


# 绘制策略曲线
def draw_equity_curve_mat(df, data_dict, date_col=None, right_axis=None, pic_size=[16, 9], font_size=25,
                          log=False, chg=False, title=None, y_label='净值'):
    """
    绘制策略曲线
    :param df: 包含净值数据的df
    :param data_dict: 要展示的数据字典格式：｛图片上显示的名字:df中的列名｝
    :param date_col: 时间列的名字，如果为None将用索引作为时间列
    :param right_axis: 右轴数据 ｛图片上显示的名字:df中的列名｝
    :param pic_size: 图片的尺寸
    :param font_size: 字体大小
    :param chg: datadict中的数据是否为涨跌幅，True表示涨跌幅，False表示净值
    :param log: 是都要算对数收益率
    :param title: 标题
    :param y_label: Y轴的标签
    :return:
    """
    # 复制数据
    draw_df = df.copy()
    # 模块基础设置
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 定义使用的字体，是个数组。
    plt.rcParams['axes.unicode_minus'] = False
    # plt.style.use('dark_background')

    plt.figure(figsize=(pic_size[0], pic_size[1]))
    # 获取时间轴
    if date_col:
        time_data = draw_df[date_col]
    else:
        time_data = draw_df.index
    # 绘制左轴数据
    for key in data_dict:
        if chg:
            draw_df[data_dict[key]] = (draw_df[data_dict[key]] + 1).fillna(1).cumprod()
        if log:
            draw_df[data_dict[key]] = np.log(draw_df[data_dict[key]].apply(float))
        plt.plot(time_data, draw_df[data_dict[key]], linewidth=2, label=str(key))
    # 设置坐标轴信息等
    plt.ylabel(y_label, fontsize=font_size)
    plt.legend(loc=2, fontsize=font_size)
    plt.tick_params(labelsize=font_size)
    plt.grid()
    if title:
        plt.title(title, fontsize=font_size)

    # 绘制右轴数据
    if right_axis:
        # 生成右轴
        ax_r = plt.twinx()
        # 获取数据
        key = list(right_axis.keys())[0]
        ax_r.plot(time_data, draw_df[right_axis[key]], 'y', linewidth=1, label=str(key))
        # 设置坐标轴信息等
        ax_r.set_ylabel(key, fontsize=font_size)
        ax_r.legend(loc=1, fontsize=font_size)
        ax_r.tick_params(labelsize=font_size)
    plt.show()


def draw_equity_curve_plotly(df, data_dict, date_col=None, right_axis=None, pic_size=[1500, 800], log=False, chg=False,
                             title=None, path=root_path + '/data/pic.html', show=True):
    """
    绘制策略曲线
    :param df: 包含净值数据的df
    :param data_dict: 要展示的数据字典格式：｛图片上显示的名字:df中的列名｝
    :param date_col: 时间列的名字，如果为None将用索引作为时间列
    :param right_axis: 右轴数据 ｛图片上显示的名字:df中的列名｝
    :param pic_size: 图片的尺寸
    :param chg: datadict中的数据是否为涨跌幅，True表示涨跌幅，False表示净值
    :param log: 是都要算对数收益率
    :param title: 标题
    :param path: 图片路径
    :param show: 是否打开图片
    :return:
    """
    draw_df = df.copy()

    # 设置时间序列
    if date_col:
        time_data = draw_df[date_col]
    else:
        time_data = draw_df.index

    # 绘制左轴数据
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for key in data_dict:
        if chg:
            draw_df[data_dict[key]] = (draw_df[data_dict[key]] + 1).fillna(1).cumprod()
        fig.add_trace(go.Scatter(x=time_data, y=draw_df[data_dict[key]], name=key, mode='lines'))

    # 绘制右轴数据
    if right_axis:
        key = list(right_axis.keys())[0]
        fig.add_trace(go.Scatter(x=time_data, y=draw_df[right_axis[key]], name=key + '(右轴)',
                                 marker=dict(color='rgba(220, 220, 220, 0.8)'), yaxis='y2'))  # 标明设置一个不同于trace1的一个坐标轴
    fig.update_layout(template="none", width=pic_size[0], height=pic_size[1], title_text=title, hovermode='x')
    # 是否转为log坐标系
    if log:
        fig.update_layout(yaxis_type="log")
    plot(figure_or_data=fig, filename=path, auto_open=False)

    # 打开图片的html文件，需要判断系统的类型
    if show:
        res = os.system('start ' + path)
        if res != 0:
            os.system('open ' + path)


def trans_period_for_grid(data, period, exg_dict=None):
    """
    周期转换函数，网格策略要用到的
    :param data: K线数据
    :param period: 数据转换周期
    :param exg_dict: 转换规则
    :return:
    """
    data = data.copy()
    data['time'] = data['candle_begin_time']
    data.set_index('candle_begin_time', inplace=True)
    agg_dict = {
        'time': 'last',
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'symbol': 'last',
    }
    if exg_dict:
        agg_dict = dict(agg_dict, **exg_dict)
    period_df = data.resample(rule=period, base=offset).agg(agg_dict)
    return period_df


def factor_info_to_str(f_infos):
    """
    将dict格式的因子新信息转为str格式。
    例如：
    输入：{'bias_3': True, '涨跌幅': True}
    输出：bias_3True+涨跌幅True
    :param f_infos:
    :return:
    """
    infos = ''
    for f in f_infos.keys():
        info = f + str(f_infos[f]) + '+'
        infos += info
    infos = infos[:-1]
    return infos


# 计算策略评价指标
def strategy_evaluate(pos_data, date='交易日期', nv_col='net_value'):
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
    start_date = temp[temp[date] <= end_date].sort_values(by=nv_col, ascending=False).iloc[0][date]
    # 将无关的变量删除
    temp.drop(['max2here', 'dd2here'], axis=1, inplace=True)
    results.loc[0, '最大回撤'] = num_to_pct(max_draw_down)
    results.loc[0, '最大回撤开始时间'] = str(start_date)
    results.loc[0, '最大回撤结束时间'] = str(end_date)

    # ===年化收益/回撤比：我个人比较关注的一个指标
    results.loc[0, '年化收益/回撤比'] = round(annual_return / abs(max_draw_down), 2)

    # ===统计每个周期
    results.loc[0, '盈利周期数'] = len(temp.loc[temp['当周期涨跌幅'] > 0])  # 盈利笔数
    results.loc[0, '亏损周期数'] = len(temp.loc[temp['当周期涨跌幅'] <= 0])  # 亏损笔数
    results.loc[0, '胜率'] = num_to_pct(results.loc[0, '盈利周期数'] / len(temp))  # 胜率
    results.loc[0, '每周期平均收益'] = num_to_pct(temp['当周期涨跌幅'].mean())  # 每笔交易平均盈亏
    results.loc[0, '盈亏收益比'] = round(temp.loc[temp['当周期涨跌幅'] > 0]['当周期涨跌幅'].mean() / \
                                    temp.loc[temp['当周期涨跌幅'] <= 0]['当周期涨跌幅'].mean() * (-1), 2)  # 盈亏比
    results.loc[0, '单周期最大盈利'] = num_to_pct(temp['当周期涨跌幅'].max())  # 单笔最大盈利
    results.loc[0, '单周期大亏损'] = num_to_pct(temp['当周期涨跌幅'].min())  # 单笔最大亏损

    # ===连续盈利亏损
    results.loc[0, '最大连续盈利周期数'] = max(
        [len(list(v)) for k, v in itertools.groupby(np.where(temp['当周期涨跌幅'] > 0, 1, np.nan))])  # 最大连续盈利次数
    results.loc[0, '最大连续亏损周期数'] = max(
        [len(list(v)) for k, v in itertools.groupby(np.where(temp['当周期涨跌幅'] <= 0, 1, np.nan))])  # 最大连续亏损次数

    return results.T
