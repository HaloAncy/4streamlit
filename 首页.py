import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
from datetime import datetime
import runpy

# 多页面
# your_working_directory/
# ├── pages/
# │   ├── a_page.py
# │   └── another_page.py
# └── your_homepage.py
# streamlit run your_homepage.py

# ppt part
st.markdown("## 题目")
st.markdown("#### 基于期货价格预测的可视化分析")
st.markdown("## 小组成员")
st.markdown("安崇毅 许龙飞")

st.markdown("## 故事背景")
st.markdown("在金融市场中，期货交易是一种常见的投资方式，投资者可以通过交易期货合约来获利。")
st.markdown("通过使用数据分析和深度学习的方法来预测某个期货品种的价格走势，来帮助他们做出更准确的交易决策。")
st.markdown("为实现该目标，我们收集了几种期货的历史价格数据集，这些数据集包含了多个指标和参数。")
st.markdown("要对某种材料的期货价格进行分析和预测，根据该材料和上游材料以及相关的期货价格的时间序列数据进行。")

st.markdown("## 主要工作")
st.markdown("1 编写爬虫爬取数据")
st.markdown("2 利用plotly来可视化分析数据集")
st.markdown("3 利用期货历史数据进行价格预测")
st.markdown("4 利用streamlit生成web页面")

st.markdown("## 数据来源")
st.markdown("英为财情：https://cn.investing.com/")
st.markdown("通过爬虫获取到以下数据集：")
st.write([
    "WTI原油期货历史数据.csv", "伦敦布伦特原油期货历史数据.csv", "黄金期货历史数据.csv", "白银期货历史数据.csv",
    "铜期货历史数据.csv", "天然气期货历史数据.csv", "美国标准普尔500指数历史数据.csv"
])

# 侧边栏
st.sidebar.markdown("## 当前日期")
current_date = datetime.now().strftime("%Y-%m-%d")
st.sidebar.write(current_date)
st.sidebar.markdown("## 数据起始日期")
st.sidebar.write("2015-01-01")
st.sidebar.markdown("## 数据最新日期")
date_filename = 'endtime.pickle'
if os.path.exists(date_filename):
    # 文件存在 读取
    with open(date_filename, 'r') as file:
        end_date = file.read().strip()  # strip()用于移除可能的空白字符
    if not end_date:  # 文件为空
        st.sidebar.write("暂无数据。")
    else:  # 文件非空
        st.sidebar.write(end_date)
else:  # 文件不存在
    st.sidebar.write("暂无数据。")

if st.sidebar.button('爬取最新数据'):
    with st.spinner('爬取中...'):
        runpy.run_path("data_spider.py")
        st.sidebar.write("爬取完成")

# 创建一个按钮，当点击时会触发页面刷新
if st.sidebar.button('刷新'):
    # 这个条件会立即被评估为True，因此页面会立即刷新
    with st.empty():
        pass  # 这里什么也不做，只是为了触发页面刷新
