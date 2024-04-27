import streamlit as st
from PIL import Image

# ppt part
st.markdown("## 预测目标")
st.markdown("预测某种原材料的实际价格，利用其对应的期货价格进行分析预测")
st.markdown("**实际价格和期货价格对比：**")

image = Image.open('1.png')
st.image(image, width=1000)

st.markdown("**数据集预测结果及实际价格对比：**")

image = Image.open('2.png')
st.image(image, width=1000)

st.markdown(
    "预测结果表明，就结合利用原油期货价格历史数据和原材料期货价格历史数据进行原材料期货价格的预测可以在大体趋势上准确预测，并且做到了基本贴近真实测试数据，\
            接下来，可以进一步结合更多的因素比如供需关系、大宗物资现价及更多期货价格等进行综合性预测，寻求最佳的时间窗口及网络层数，找寻更优性能的模型。"
)
