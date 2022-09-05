"""
花式网格船队 第2期 | 邢不行 | 2022分享会
author: 邢不行
微信: xbx6660
"""
import numpy as np

# =网格参数
current = 100  # 当前价格
grid_range = (0.5, 0.6)
low = current * (1 - grid_range[0])  # 网格下限
high = current * (1 + grid_range[1])  # 网格上限
grid_num = 90  # 网格数量
cap = 10000  # 开仓金额
leverage = 3  # 杠杆
max_rate = 0.95  # 最大投资比例
c_rate = 2 / 10000  # 手续费
# ===========

# ===计算网格：每个格子的价格序列
# 等比网格规律：网格最低价 x q^n = 最高价，q为等比比例(q>1)，n为网格数目count
# 所以q = (最高价 / 最低价) ** (1 / n)
q = (high / low) ** (1 / grid_num)
price_array = []
for i in range(0, grid_num + 1):
    price_array.append(low * (q ** i))
price_array = np.array(price_array).round(8)
print(price_array)

# 查找废弃的那个格子
del_index = np.argmin(abs(price_array - current))
# 正式的网格
grid_array = np.delete(price_array, del_index)
# 每格子可以买几个币, 这里忽略了单币种最小下单量
order_num = cap * leverage * max_rate / price_array.sum()

# 下破网
low_price = grid_array[0]
# 破网的格子数
grids = np.sum(grid_array <= current)
# 持仓均价
mean_price = np.mean(grid_array[:del_index])
# 破网持仓价格
break_price = mean_price * grids * order_num
# 破网亏损
loss = break_price - grids * low_price * order_num
# 手续费
rate = break_price * c_rate
# 亏损比例
low_loss_rate = (loss + rate) / cap
print('下破网亏损比例: ', low_loss_rate)

# 上破网
high_price = grid_array[-1]
# 破网的格子数
grids = np.sum(grid_array >= current)
# 持仓均价
mean_price = np.mean(grid_array[del_index:])
# 破网持仓价格
break_price = mean_price * grids * order_num
# 破网亏损
loss = grids * high_price * order_num - break_price
# 手续费
rate = break_price * c_rate
# 亏损比例
up_loss_rate = (loss + rate) / cap
print('上破网亏损比例: ', up_loss_rate)
print(f'网格数:{grid_num}  杠杆:{leverage}  区间:{grid_range}')
