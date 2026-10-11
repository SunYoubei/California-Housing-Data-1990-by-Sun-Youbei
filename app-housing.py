import streamlit as st
import pandas as pd

# ---------- 页面配置 ----------
st.set_page_config(page_title="California Housing Data", layout="wide")

# ---------- 加载数据 ----------
@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    return df

df = load_data()

# ---------- 标题 ----------
st.title("California Housing Data (1990) by 你的姓名")

# ---------- 滑块：筛选 median_house_value ----------
min_value = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000
)

# 根据滑块过滤数据
filtered_df = df[df["median_house_value"] >= min_value]

# ---------- 侧边栏子标题 ----------
st.subheader("See more filters in the sidebar:")

# ---------- 侧边栏多选：筛选 ocean_proximity ----------
all_locations = df["ocean_proximity"].unique().tolist()
selected_locations = st.sidebar.multiselect(
    "Choose the location type",
    options=all_locations,
    default=all_locations
)

# ---------- 侧边栏单选：筛选 median_income ----------
income_level = st.sidebar.radio(
    "Choose income level",
    options=["All", "Low", "Medium", "High"]
)

# 根据收入水平过滤
if income_level == "Low":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "Medium":
    filtered_df = filtered_df[
        (filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] <= 5.0)
    ]
elif income_level == "High":
    filtered_df = filtered_df[filtered_df["median_income"] > 5.0]

# 根据地理位置类型过滤
filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(selected_locations)]

# ---------- 显示地图 ----------
st.map(filtered_df, latitude="latitude", longitude="longitude")

# ---------- 显示过滤后的数据摘要 ----------
st.write(f"显示 {len(filtered_df)} 条记录（共 {len(df)} 条）")