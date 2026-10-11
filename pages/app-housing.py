import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. 页面基础配置
# ==========================================
st.set_page_config(page_title="California Housing Data", layout="wide")

# 设置标题，名字改为 Sun Youbei
st.title("California Housing Data (1990) by Sun Youbei")

# ==========================================
# 2. 读取数据 (使用缓存加速)
# ==========================================
@st.cache_data
def load_data():
    # 与 app-housing.py 在同一目录下，直接读取文件名
    df = pd.read_csv("housing.csv")
    return df

df = load_data()

# ==========================================
# 3. 侧边栏筛选 (完全参照图3)
# ==========================================
# 侧边栏：地理位置多选 (默认全选)
locations = df["ocean_proximity"].unique().tolist()
selected_locations = st.sidebar.multiselect(
    "Choose the location type",
    options=locations,
    default=locations
)

# 侧边栏：收入水平单选 (图3没有 All 选项，直接从 Low 开始)
income_level = st.sidebar.radio(
    "Choose income level",
    options=["Low", "Medium", "High"]
)

# ==========================================
# 4. 数据过滤逻辑
# ==========================================
# 先根据地理位置过滤
filtered_df = df[df["ocean_proximity"].isin(selected_locations)]

# 再根据收入水平过滤 (按 tutorial 里的阈值)
if income_level == "Low":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "Medium":
    filtered_df = filtered_df[
        (filtered_df["median_income"] > 2.5) & 
        (filtered_df["median_income"] <= 5.0)
    ]
elif income_level == "High":
    filtered_df = filtered_df[filtered_df["median_income"] > 5.0]

# ==========================================
# 5. 主界面：地图展示
# ==========================================
# 绘制加州地图
st.map(filtered_df, latitude="latitude", longitude="longitude")

# ==========================================
# 6. 主界面：直方图展示
# ==========================================
st.subheader("Histogram of Median House Value")

# 使用 matplotlib 绘制直方图
fig, ax = plt.subplots(figsize=(10, 4))
# 绘制 histogram，颜色使用图3类似的蓝色
ax.hist(filtered_df["median_house_value"], bins=30, color="royalblue", edgecolor="white")
ax.set_xlabel("Median House Value")
ax.set_ylabel("Number of Districts")

# 在 Streamlit 中显示图表
st.pyplot(fig)
