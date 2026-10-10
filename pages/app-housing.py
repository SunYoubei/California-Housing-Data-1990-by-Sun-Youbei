import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8')

st.title('California Housing Data (1990) by Minghong Xiong')

df = pd.read_csv('housing.csv')

# slider in the main area: keep districts whose median house value is at least this value
value_filter = st.slider('Minimal Median House Value', 0, 500001, 200000)  # min, max, default

st.subheader('See more filters in the sidebar:')

# sidebar multiselect: filter by location type, all selected by default
location_filter = st.sidebar.multiselect(
    'Choose the location type',
    df.ocean_proximity.unique(),   # options
    df.ocean_proximity.unique())   # defaults

# sidebar radio: filter by income level
income_filter = st.sidebar.radio(
    'Choose income level',
    ('Low', 'Medium', 'High'))

# filter by median house value
df = df[df.median_house_value >= value_filter]

# filter by location type
df = df[df.ocean_proximity.isin(location_filter)]

# filter by income level
if income_filter == 'Low':
    df = df[df.median_income <= 2.5]
elif income_filter == 'Medium':
    df = df[(df.median_income > 2.5) & (df.median_income < 4.5)]
elif income_filter == 'High':
    df = df[df.median_income >= 4.5]

# show on map
st.map(df)

# show the histogram below the map
st.subheader('Histogram of Median House Value')
fig, ax = plt.subplots(figsize=(20, 5))
ax.hist(df.median_house_value, bins=30)
ax.set_xlabel('Median House Value')
ax.set_ylabel('Number of Districts')
st.pyplot(fig)
