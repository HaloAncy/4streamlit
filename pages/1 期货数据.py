import streamlit as st
import pandas as pd
import numpy as np
import randomcolor
import plotly.figure_factory as ff
import plotly.express as px
import plotly.graph_objs as go
from scipy.stats import zscore

dataname_list = [
    "WTIoil", "LBoil", "gold", "silver", "copper", "natural_gas", "SPX"
]
datafile_list = [
    "WTI原油期货历史数据.csv", "伦敦布伦特原油期货历史数据.csv", "黄金期货历史数据.csv", "白银期货历史数据.csv",
    "铜期货历史数据.csv", "天然气期货历史数据.csv", "美国标准普尔500指数历史数据.csv"
]
name_dict = dict(zip(dataname_list, datafile_list))
file_path = "C:\\baiduTB\\BaiduSyncdisk\\workspace\\workspace for py\\YCproject\\update\\"

st.set_page_config(layout="wide")  # 居中布局

st.sidebar.markdown("# 期货数据情况")

# 单期货选择
choice = st.sidebar.selectbox(
    label='请选择期货名称',
    options=(dataname_list),
    index=0,  # 默认选项
    format_func=str,
    help='nothing')
extract_data = pd.read_csv(name_dict[choice])
st.markdown("**数据集Dataframe结构：**")
st.dataframe(extract_data)
df = extract_data
df['涨跌幅'] = df['涨跌幅'].str.replace("%", "").astype(float)

# 收盘+开盘
fig = px.line(extract_data,
              x="日期",
              y=extract_data.columns[1:3],
              hover_data={"日期"},
              title=choice + "期货")
fig.update_xaxes(rangeslider_visible=True)  # range slider
fig.update_xaxes(minor=dict(ticks="inside", showgrid=True))
fig.update_layout(yaxis_title='价格')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("折线图由横轴和纵轴组成，横轴表示时间，纵轴表示价格。每个数据点由收盘价或开盘价组成，通过连接这些数据点形成折线图。")
st.markdown("观察横轴上的时间刻度和纵轴上的价格刻度，可以跟踪价格的变化趋势。")
st.markdown("通过分析，用户可以获得关于价格趋势、日内波动和买入卖出力量的重要信息，以指导他们的投资决策和交易策略。")
# # 收盘折线
# st.line_chart(extract_data,
#               x="日期",
#               y=["收盘"],
#               color=[randomcolor.RandomColor().generate()[0]],
#               width=1080,
#               height=550)  # 随机颜色

# 价格差
df['价格差'] = df['高'] - df['低']
fig = px.box(df, x='日期', y='价格差', title='每日价格波动区间')
fig.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig, use_container_width=True)
# 收盘价和开盘价之间的连线表示了每个交易日价格的变化情况。
# ppt
st.markdown("每日最高最低价格差图由横轴和纵轴组成，横轴表示时间，纵轴表示价格差。每个数据点表示每个交易日的最高价格和最低价格之间的差异。")
st.markdown("观察横轴上的时间刻度和纵轴上的价格差刻度，可以跟踪价格差的变化趋势。较高的数据点表示价格差较大，较低的数据点表示价格差较小。")
st.markdown("通过分析，用户可以获得关于市场波动性、趋势和极端波动的重要信息，以帮助他们评估市场风险、制定交易策略和管理投资组合。")


def convert_k_to_number(s):  # 转换"K"格式的字符串为数字
    if pd.isna(s):
        return 0
    number_str = ''.join(filter(str.isdigit, s)) + '.'
    whole, decimal = number_str.split('.')
    return float(whole + decimal) * 1000


# 交易量柱线
choose_data = extract_data[["日期", "交易量"]]
choose_data.loc[:, '交易量'] = choose_data['交易量'].apply(convert_k_to_number)
# st.dataframe(choose_data)
# st.bar_chart(choose_data,
#              x="日期",
#              y=["交易量"],
#              color=[randomcolor.RandomColor().generate()[0]])

fig = px.bar(
    choose_data,
    x='日期',
    y='交易量',
    title='交易量柱状图',
)
fig.update_xaxes(rangeslider_visible=True)
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("交易量柱状图由横轴和纵轴组成，横轴表示时间，纵轴表示交易量。每个数据点由一个垂直的柱状图表示，柱状图的高度表示该交易日的交易量。")
st.markdown("观察横轴上的时间刻度和纵轴上的交易量刻度，可以跟踪交易量的变化趋势。较高的柱状图表示交易量较大，较低的柱状图表示交易量较小。")
st.markdown("通过分析，用户可以获得关于交易量趋势、交易活跃度和交易量异常的重要信息，以帮助他们评估市场情况、预测价格变动和制定交易策略。")

# 涨跌幅
# chg_data = extract_data[["日期", "涨跌幅"]]
# chg_data['涨跌幅'] = chg_data['涨跌幅'].str.replace("%", "").astype(float)
# fig = px.box(chg_data, x="日期", y="涨跌幅")
# fig.update_traces(quartilemethod="exclusive")
# st.plotly_chart(fig, use_container_width=True)

# fig = px.histogram(
#     df,
#     x='涨跌幅',
#     nbins=500,
#     title='期货涨跌幅分布',
# )
# st.plotly_chart(fig, use_container_width=True)

# add lines
df['日期'] = pd.to_datetime(df['日期'])
df['Day'] = df['日期'].dt.day
df['Week'] = df['日期'].dt.isocalendar().week
df['Year'] = df['日期'].dt.year
df['Month'] = df['日期'].dt.month

# 将数据按周划分并计算每周平均收盘价
weekly_avg = df.groupby(['Year', 'Week'])['收盘'].mean().reset_index()
fig = px.line(weekly_avg, x="Week", y="收盘", color="Year", title='每周平均收盘价')
fig.update_yaxes(title_text='平均收盘价')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("每周平均收盘价图由横轴和纵轴组成，横轴表示时间，纵轴表示价格。每个数据点由每周的平均收盘价组成。")
st.markdown("观察横轴上的时间刻度和纵轴上的价格刻度，可以了解每周平均收盘价的变化趋势。通过连接数据点的线条，可以观察价格在不同周之间的变化。")
st.markdown("通过分析，用户可以获得关于周趋势、周波动和季节性趋势的重要信息，以帮助他们评估市场走势、制定交易策略和进行长期投资规划。")

# 计算每个月的平均收盘价
monthly_avg = df.groupby(['Year', 'Month'])['收盘'].mean().reset_index()
fig = px.line(monthly_avg, x="Month", y="收盘", color="Year", title='每月平均收盘价')
fig.update_yaxes(title_text='平均收盘价')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("每月平均收盘价图由横轴和纵轴组成，横轴表示时间，纵轴表示价格。每个数据点代表每个月的平均收盘价。")
st.markdown(
    "观察横轴上的时间刻度和纵轴上的价格刻度，可以了解每月平均收盘价的变化趋势。通过连接数据点的线条，可以观察价格在不同月份之间的变化。")
st.markdown("通过分析，用户可以获得关于月趋势、月波动和季节性趋势的重要信息，以帮助他们评估市场走势、制定交易策略和进行长期投资规划。")

# 计算每年的平均收盘价
avg_closing_per_year = df.groupby('Year')['收盘'].mean().reset_index()
fig = px.bar(avg_closing_per_year, x='Year', y='收盘', title='年度平均收盘价')
fig.update_yaxes(title_text='平均收盘价')
fig.update_xaxes(showticklabels=True)
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("每年平均收盘价图由横轴和纵轴组成，横轴表示时间，纵轴表示价格。每个数据点代表每年的平均收盘价。")
st.markdown(
    "观察横轴上的时间刻度和纵轴上的价格刻度，可以了解每年平均收盘价的变化趋势。通过连接数据点的线条，可以观察价格在不同年份之间的变化。")
st.markdown("通过分析，用户可以获得关于年趋势、年波动和长期趋势的重要信息，以帮助他们评估市场走势、制定长期投资策略和进行风险管理。")

# 使用pivot来创建一个适合热图的数据格式
heatmap_data = df.pivot_table(values='收盘',
                              index=df['Day'],
                              columns=df['Month'],
                              aggfunc='mean')
fig = px.imshow(heatmap_data, title='每日收盘价月度热图')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("每日收盘价月度热图由横轴和纵轴组成，横轴表示月份，纵轴表示日期。每个数据单元格的颜色表示相应日期和月份的收盘价。")
st.markdown(
    "观察横轴上的月份和纵轴上的日期，可以定位到每个数据单元格。通过观察单元格的颜色，可以了解收盘价的相对高低。较高的收盘价通常用较深的颜色表示，而较低的收盘价则用较浅的颜色表示。"
)
st.markdown(
    "通过分析，用户可以获得关于月度趋势(整体色调)、日趋势(单元格颜色)和异常值(单元格颜色的异常变化)的重要信息，以帮助他们评估股票或其他金融产品的价格走势、发现潜在的交易机会和管理风险。"
)

# 不同年份收盘价的箱形图分析
# 比较不同年份的价格分布情况，了解市场的波动范围
fig = px.box(df, x='Year', y='收盘', title='收盘价分布')
fig.update_xaxes(title_text='年份')
fig.update_yaxes(title_text='收盘价')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("不同年份收盘价的箱形图由横轴和纵轴组成，横轴表示年份，纵轴表示收盘价。每个箱形图代表一个年份的收盘价分布。")
st.markdown(
    "观察横轴上的年份和纵轴上的收盘价范围，可以定位到每个箱形图。通过观察箱形图的各个部分，可以了解收盘价的分布情况。箱体的长度表示收盘价的四分位距离，箱体中间的线表示中位数。箱形图的上边界和下边界表示收盘价的最大值和最小值。异常值的标记可能表示收盘价中的离群值。"
)
st.markdown(
    "通过分析不同年份收盘价的箱形图，用户可以获得关于年度分布(箱形图的位置和形态)、年度波动(箱体长度和上下边界的距离)和异常值的重要信息，以帮助他们比较不同年份的收盘价分布、评估收盘价的稳定性和发现特殊情况。"
)

# 识别极端涨跌幅
extreme_moves = df[df['涨跌幅'].abs() > df['涨跌幅'].quantile(0.95)]
fig = px.scatter(extreme_moves, x='日期', y='涨跌幅', color='涨跌幅', title='极端涨跌幅日期')
fig.update_xaxes(title_text='日期')
fig.update_yaxes(title_text='涨跌幅 (%)')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("识别极端涨跌幅由时间轴和价格变动幅度组成。价格变动幅度显示涨幅和跌幅的极端情况。")
st.markdown("观察时间轴上的时间点和价格变动幅度点，可以了解价格的变动情况。特别关注离群的数值点，它们表示了极端的涨跌幅情况。")
st.markdown(
    "通过分析，用户可以获得关于价格的极端变动日期以及价格趋势的重要信息。这有助于用户了解股票或金融产品在不同时间段内的价值波动，并可能提供交易或投资决策的参考。"
)

# 交易量加权平均价格(VWAP)分析
# VWAP是一个重要的交易指标，可用于了解交易者的行为。
df['交易量'] = df['交易量'].apply(convert_k_to_number)
df['VWAP'] = (df['交易量'] * (df['高'] + df['低'] + df['收盘']) /
              3).cumsum() / df['交易量'].cumsum()
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['日期'], y=df['VWAP'], mode='lines', name='VWAP'))
fig.update_layout(title='期货成交量加权平均价格 (VWAP) ',
                  xaxis_title='日期',
                  yaxis_title='VWAP')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown(
    "交易量加权平均价格(VWAP)分析图由时间轴和VWAP线组成。VWAP线表示在特定时间段内的平均交易价格，根据交易量加权计算得出。")
st.markdown(
    "观察时间轴上的时间点和VWAP线的走势，可以了解交易价格的平均水平。VWAP线上升表示交易价格偏高，VWAP线下降表示交易价格偏低。")
st.markdown(
    "通过分析，用户可以获得关于交易价格平均水平(VWAP线整体走势)、相对价值(比较实际交易价格与VWAP线的关系)和交易趋势(交易价格的整体趋势)的重要信息。这有助于用户了解股票或金融产品的交易价格动态，并可能为交易决策提供参考。"
)

# 月度涨跌幅分析
# 分析每月的涨跌幅度，找出哪些月份市场波动性更大。
avg_change_per_month = df.groupby('Month')['涨跌幅'].mean().reset_index()
fig = px.line(avg_change_per_month, x='Month', y='涨跌幅', title='月度平均涨跌幅')
fig.update_yaxes(title_text='平均涨跌幅 (%)')
fig.update_xaxes(tickmode='array',
                 tickvals=list(range(1, 13)),
                 title_text='月份')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("月度涨跌幅分析由时间轴和涨跌幅度组成。每个月份对应一个涨跌幅度，可以显示价格在不同月份的涨跌情况。")
st.markdown("观察时间轴上的月份和涨跌幅度的线条或柱状图，可以了解不同月份的价格涨跌情况。正值的涨跌幅表示价格上涨，负值的涨跌幅表示价格下跌。")
st.markdown(
    "通过分析，用户可以获得关于价格涨跌趋势(正负值和其走势)、极端涨跌情况(涨跌幅度最值)和季节性影响的重要信息。这有助于用户了解股票或金融产品在不同月份内的价格变动情况，并可能提供投资或交易决策的参考。"
)

# 涨跌幅随时间的累积效应
# 计算并展示涨跌幅随时间累积的效应，以了解长期趋势。
df['累计涨跌幅'] = df['涨跌幅'].cumsum()
fig = px.line(df, x='日期', y='累计涨跌幅', title='涨跌幅累计效应')
fig.update_yaxes(title_text='累计涨跌幅 (%)')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("涨跌幅随时间的累积效应图由时间轴和累积涨跌幅度组成。累积涨跌幅度表示从起始时间到当前时间的总体涨跌情况。")
st.markdown(
    "观察时间轴上的时间点和累积涨跌幅度的线条或曲线，可以了解涨跌幅在时间累积下的影响。正值的累积涨跌幅表示总体上的涨幅，负值的累积涨跌幅表示总体上的跌幅。"
)
st.markdown(
    "通过分析，用户可以获得关于涨跌幅随时间的总体趋势、叠加效应和长期趋势评估的重要信息。这有助于用户了解股票或金融产品在时间累积下的涨跌情况，并可能提供投资或交易决策的参考。"
)

# 涨跌幅的时间热点
# 使用pivot创建涨跌幅的热图数据格式
change_heatmap_data = df.pivot_table(values='涨跌幅',
                                     index=df['Day'],
                                     columns=df['Month'],
                                     aggfunc='mean')
fig = px.imshow(change_heatmap_data, title='每日涨跌幅月度热图')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown(
    "涨跌幅的时间热度分布图由时间轴和热度图组成。热度图以颜色或其他形式表示不同时间段内的涨跌幅度，用于展示涨跌幅的时间热点和分布情况。")
st.markdown(
    "观察时间轴上的时间段和热度图中的颜色或形状，可以了解不同时间段内涨跌幅度的热度分布。较亮或突出的颜色表示较大的涨幅，较暗或次要的颜色表示较大的跌幅。"
)
st.markdown(
    "通过分析，用户可以获得关于时间热点(颜色的分布情况)、高频波动(颜色的密集程度)和季节性趋势的重要信息。这有助于用户了解股票或金融产品在不同时间段内涨跌幅的分布情况，并可能提供投资或交易决策的参考。"
)

# 收盘价季节性分析
# 评估原油价格是否存在季节性模式。
df['季节'] = df['日期'].dt.month % 12 // 3 + 1
seasonal_trends = df.groupby(['Year', '季节'])['收盘'].mean().unstack()
fig = px.line(seasonal_trends, title='期货季节性价格趋势')
fig.update_xaxes(title_text='年份')
fig.update_yaxes(title_text='平均收盘价')
fig.update_layout(legend_title_text='季节')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("价格季节性分析图由时间轴和统计折线图组成，用于显示收盘价在不同季节性时段的趋势和分布。")
st.markdown("观察时间轴上的季节性时段和折线图，可以了解收盘价在不同季节性时段内的趋势和分布情况。")
st.markdown(
    "通过分析，用户可以获得关于季节性趋势、偏离情况和分布情况的重要信息。这有助于用户了解股票或金融产品在不同季节性时段内收盘价的变动情况，并可能提供投资或交易决策的参考。"
)

# 计算季度平均交易量
quarterly_volume_avg = df.groupby(['Year', '季节'])['交易量'].mean().unstack()
fig = px.line(quarterly_volume_avg, title='季度平均交易量趋势')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("季度平均交易量图由时间轴和折线图组成，用于显示不同季度的平均交易量水平。")
st.markdown("观察时间轴上的季度时间段和折线图，可以了解不同季度的平均交易量水平。")
st.markdown(
    "通过分析，用户可以获得关于季度交易活跃度、交易趋势和交易峰值的重要信息。这有助于用户了解股票或金融产品在不同季度内的交易量变动情况，并可能提供投资或交易决策的参考。"
)

# 移动平均线分析
# 使用移动平均线来平滑价格数据，以识别长期趋势。
# 计算20日和50日移动平均线
df['MA20'] = df['收盘'].rolling(window=20).mean()
df['MA50'] = df['收盘'].rolling(window=50).mean()
fig = go.Figure()
# 绘制收盘价
fig.add_trace(go.Scatter(x=df['日期'], y=df['收盘'], mode='lines', name='收盘价'))
# 绘制20日移动平均线
fig.add_trace(go.Scatter(x=df['日期'], y=df['MA20'], mode='lines', name='20日MA'))
# 绘制50日移动平均线
fig.add_trace(go.Scatter(x=df['日期'], y=df['MA50'], mode='lines', name='50日MA'))
fig.update_layout(title='期货收盘价与移动平均线', xaxis_title='日期', yaxis_title='价格')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("移动平均线分析图由价格线图和移动平均线组成，用于分析价格的长期趋势和短期波动。")
st.markdown(
    "观察价格线图和移动平均线的交叉和走势，可以进行移动平均线分析。移动平均线可以显示价格的长期趋势和短期波动。交叉点、斜率和距离等因素可以提供价格走势的信息。"
)
st.markdown("通过分析，可以帮助用户了解价格的趋势、支撑和阻力水平以及交叉信号。这有助于用户进行趋势判断、确定买入卖出时机和制定风险管理策略。")
st.markdown(
    "- 观察移动平均线的走势，可以判断价格的长期趋势。当价格线从下方穿过移动平均线并向上运动，可能表明价格趋势为上涨；而当价格线从上方穿过移动平均线并向下运动，可能表明价格趋势为下跌。"
)
st.markdown(
    "- 移动平均线可以显示价格的支撑和阻力水平。当价格在移动平均线上方运动时，移动平均线可能成为支撑水平；当价格在移动平均线下方运动时，移动平均线可能成为阻力水平。"
)
st.markdown(
    "- 当不同周期的移动平均线交叉时，可能产生交叉信号，表明价格趋势的变化。常见的交叉信号包括短期移动平均线向上穿越长期移动平均线（金叉），表示买入信号；以及短期移动平均线向下穿越长期移动平均线（死叉），表示卖出信号。"
)

# 简单的异常点检测，例如收盘价的Z分数
df['收盘_zscore'] = zscore(df['收盘'])
anomalies = df[np.abs(df['收盘_zscore']) > 2]
fig = px.scatter(df,
                 x=df.index,
                 y='收盘',
                 color=np.abs(df['收盘_zscore']) > 2,
                 title='收盘价异常点检测')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("Z分数(标准差)通过计算每个数据点的Z分数，来确定是否存在偏离正常范围的异常点。")
st.markdown(
    "观察价格走势图和异常点标记，可以进行简单的异常点检测。通过计算每个数据点的Z分数，偏离正常范围的数据点可以被标记为异常点。这些异常点可能表示价格的异常波动或潜在的交易机会。"
)
st.markdown(
    "通过异常点检测，可以辅助投资者识别价格走势中的异常点，并可能提供交易机会或风险管理的参考。然而，这种方法是一种简单的统计分析方法，仅作为辅助工具使用，投资者应结合其他技术和基本分析进行综合判断和决策。"
)

# 计算收盘价与交易量的相关性
correlation = df[['收盘', '交易量']].corr()
fig = px.imshow(correlation, text_auto=True, title='价格与交易量的相关性分析')
st.plotly_chart(fig, use_container_width=True)
# ppt
st.markdown("计算收盘价与交易量的相关性用于探索收盘价和交易量之间的关联关系，生成相关性矩阵的热图。")
st.markdown("热图的颜色和数值表示了相关性的强度，相关系数提供了一个数值指标来衡量两者之间的线性关联程度。")
st.markdown(
    "计算收盘价与交易量的相关性可以帮助投资者了解这两个因素之间的关系。相关性分析可以提供有关市场参与者情绪、市场活跃程度和资金流动等方面的信息。然而，相关性并不代表因果关系，投资者仍需综合考虑其他因素进行决策。"
)

st.markdown("**补充信息后数据集Dataframe结构：**")
st.dataframe(df)
