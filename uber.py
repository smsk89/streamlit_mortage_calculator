"""
Пример обработки данных (Uber pickups in NYC, DataSet - 2014)
https://docs.streamlit.io/get-started/tutorials/create-an-app
"""

import streamlit as st
import pandas as pd
import numpy as np

class UberPickups:
    def __init__(self):
        self.DATE_COLUMN = 'date/time'
        self.DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
                         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

    def load_data(self, nrows):
        @st.cache_data
        def fetch_data(_nrows, _data_url, _date_column):
            data = pd.read_csv(_data_url, nrows=_nrows)
            lowercase = lambda x: str(x).lower()
            data.rename(lowercase, axis='columns', inplace=True)
            data[_date_column] = pd.to_datetime(data[_date_column])
            return data

        return fetch_data(nrows, self.DATA_URL, self.DATE_COLUMN)

    def render(self):
        st.title('Uber pickups in NYC')

        data = self.load_data(10000)

        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(data)

        st.subheader('Number of pickups by hour')
        hist_values = np.histogram(data[self.DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
        st.bar_chart(hist_values)

        hour_to_filter = st.slider('hour', 0, 23, 17)
        filtered_data = data[data[self.DATE_COLUMN].dt.hour == hour_to_filter]

        st.subheader('Map of all pickups at %s:00' % hour_to_filter)
        st.map(filtered_data)
