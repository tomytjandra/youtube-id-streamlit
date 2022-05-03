# ---------- LOAD LIBRARIES

# data analysis
import pandas as pd
import json

# data visualization
import plotly.express as px
px.defaults.template = "plotly_dark"
px.defaults.color_continuous_scale = "reds"

# dashboarding
from PIL import Image
import streamlit as st

# ---------- PAGE CONFIGURATION

st.set_page_config(
    page_title='YouTube Trending Statistics',
    page_icon='assets/youtube-icon.png',
    layout='wide')

# ---------- READ PICKLE

youtube = ___

# ---------- READ JSON

with open("data_input/category.json") as file:
    ___

# ---------- DATA WRANGLING

# map integer category_id to its corresponding name
youtube['category_id'] = ___

# take the first trending day for each videos
youtube = ___
youtube_unique = ___

# handle missing values
youtube_unique['category_id'] = ___
youtube_unique.dropna(___)

# feature engineering
youtube_unique['publish_day'] = ___
youtube_unique['publish_hour'] = ___
youtube_unique['trending_date'] = ___

# ---------- DASHBOARD SIDEBAR

# image
image = Image.open('assets/youtube.png')
st.sidebar.image(image)

# date input
min_date = ___
max_date = ___
selected_start_date, selected_end_date = st.sidebar.date_input(
    label='Trending Date Range',
    min_value=___,
    max_value=___,
    value=[___, ___])

# select box
selected_category = st.sidebar.selectbox(
    label='Video Category',
    options=___)

# ---------- FILTER DATA BASED ON USER INPUT

# filter date
youtube_unique = ___

# filter category
if selected_category != 'All Categories':
    youtube_unique = ___

# ---------- DASHBOARD BODY

# title
st.title("Indonesia's YouTube Trending Statistics")

# metrics
col1, col2 = st.columns(2)
col1.metric(label='Total Unique Videos', value=___)
col2.metric(label='Total Unique Channels', value=___)

# bar chart
st.header(':video_camera: Channels')
data = ___
fig = ___
fig.update_layout(___)
st.plotly_chart(fig)

# heatmap
st.header(':date: Publish Time')
fig = ___
fig.update_yaxes(___)
st.plotly_chart(fig)
