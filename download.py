import os
import pandas as pd
import streamlit as st
from kaggle.api.kaggle_api_extended import KaggleApi

# set secrets
os.environ['KAGGLE_USERNAME'] = st.secrets['KAGGLE_USERNAME']
os.environ['KAGGLE_KEY'] = st.secrets['KAGGLE_KEY']

def download_data():
    # connect API
    api = KaggleApi()
    api.authenticate()

    # download files
    api.dataset_download_files(
        dataset=st.secrets['KAGGLE_DATASET'],
        path='data_input',
        unzip=True)


def convert_to_pickle():
    # read csv
    columns = [
        'publish_time', 'trending_time',
        'title', 'channel_name', 'category_id',
        'view', 'like', 'dislike', 'comment']

    youtube = pd.read_csv(
        'data_input/trending.csv',
        usecols=columns,
        parse_dates=['publish_time', 'trending_time'])

    # save to pickle
    youtube.to_pickle('data_input/trending.pickle')


def main():
    download_data()
    convert_to_pickle()

main()