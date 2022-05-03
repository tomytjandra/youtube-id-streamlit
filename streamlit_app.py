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

# ---------- READ CSV

# columns = [
#     'publish_time', 'trending_time',
#     'title', 'channel_name', 'category_id',
#     'view', 'like', 'dislike', 'comment']

# youtube = pd.read_csv(
#     'data_input/trending.csv',
#     usecols=columns,
#     parse_dates=['publish_time', 'trending_time'])

# ---------- READ PICKLE

youtube = pd.read_pickle('data_input/trending.pickle')

# ---------- READ JSON

with open("data_input/category.json") as file:
    json_data = json.load(file)
    df = pd.json_normalize(json_data, record_path='items')
    df.index = df['id'].astype('int')
    category_mapping = df['snippet.title'].to_dict()

# ---------- DATA WRANGLING

# map integer category_id to its corresponding name
youtube['category_id'] = youtube['category_id'].map(category_mapping)

# take the first trending day for each videos
youtube = youtube.sort_values(by='trending_time')
youtube_unique = youtube.drop_duplicates(subset=['channel_name', 'title'], keep='first').copy()

# handle missing values
youtube_unique['category_id'] = youtube_unique['category_id'].fillna('Unknown')
youtube_unique.dropna(subset='view', inplace=True)

# feature engineering
youtube_unique['publish_day'] = youtube_unique['publish_time'].dt.day_name()
youtube_unique['publish_hour'] = youtube_unique['publish_time'].dt.hour
youtube_unique['trending_date'] = youtube_unique['trending_time'].dt.date

# ---------- DASHBOARD SIDEBAR

# image
image = Image.open('assets/youtube.png')
st.sidebar.image(image)

# date input
min_date = youtube_unique['trending_date'].min()
max_date = youtube_unique['trending_date'].max()
selected_start_date, selected_end_date = st.sidebar.date_input(
    label='Trending Date Range',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date])

# select box
selected_category = st.sidebar.selectbox(
    label='Video Category',
    options=['All Categories'] + youtube_unique['category_id'].sort_values().unique().tolist())

# # button
# update_data = st.sidebar.button(
#     label='Update Dataset',
#     help=f"Download latest dataset from [Kaggle]({st.secrets['KAGGLE_DATASET']})"
# )
# if update_data:
#     with st.spinner('Downloading dataset...'):
#         from download import main
#         main()
#     st.experimental_rerun()

# ---------- FILTER DATA BASED ON USER INPUT

# filter date
youtube_unique = youtube_unique[
    (youtube_unique['trending_date'] >= selected_start_date) &
    (youtube_unique['trending_date'] <= selected_end_date)]

# filter category
if selected_category != 'All Categories':
    youtube_unique = youtube_unique[youtube_unique['category_id'] == selected_category]

# ---------- DASHBOARD BODY

# title
st.title("Indonesia's YouTube Trending Statistics")

# metrics
col1, col2 = st.columns(2)
col1.metric(label='Total Unique Videos',
            value=youtube_unique['title'].nunique())
col2.metric(label='Total Unique Channels',
            value=youtube_unique['channel_name'].nunique())

# bar chart
st.header(':video_camera: Channels')
data = youtube_unique['channel_name'].value_counts().nlargest(10).sort_values(ascending=True)
fig = px.bar(
    data,
    orientation='h',
    title=f'Top 10 Trending Channels in {selected_category}',
    labels=dict(index='', value='Video Count'),
    color=data)
fig.update_layout(coloraxis_showscale=False, xaxis_separatethousands=True)
fig.update_traces(hovertemplate='<b>%{y}</b><br>%{x} Videos', name='')
st.plotly_chart(fig)

# heatmap
st.header(':date: Publish Time')
fig = px.density_heatmap(
    youtube_unique,
    x='publish_hour',
    y='publish_day',
    title=f'Count of Trending Videos in {selected_category}',
    labels=dict(publish_hour='Publish Hour', publish_day='Publish Day'))
fig.update_yaxes(
    categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    autorange='reversed')
fig.update_traces(hovertemplate='<b>%{y} (Hour: %{x})</b><br>%{z} Videos')
st.plotly_chart(fig)

# # scatter plot
# st.header(':bulb: Engagement')
# metric_choices = ['like', 'dislike', 'favorite', 'comment']
# col1, col2 = st.columns(2)
# var_x = col1.selectbox(label='Horizontal Axis',
#                        options=metric_choices, index=0)
# var_y = col2.selectbox(label='Vertical Axis', options=metric_choices, index=1)

# fig = px.scatter(
#     youtube_unique,
#     x=var_x,
#     y=var_y,
#     size='view',
#     title=f'{var_x.title()} vs {var_y.title()} in {selected_category}',
#     hover_name='channel_name',
#     hover_data=['title'])
# st.plotly_chart(fig)