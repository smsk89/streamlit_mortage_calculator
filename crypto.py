import streamlit as st
import pandas as pd
import base64
import requests
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

load_dotenv()
API_KEY = os.getenv('CRYPTO_API_KEY')

API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

parameters = {
    'start': '1',
    'limit': '200',     # количество запрашиваемых криптовалют
    'convert': 'USD'
}

st.set_page_config(layout="wide")


class CryptoData:
    @st.cache_data
    def load_data(_self):
        response = requests.get(API_URL, headers=headers, params=parameters)
        data = response.json()

        coin_name = []
        coin_symbol = []
        market_cap = []
        percent_change_1h = []
        percent_change_24h = []
        percent_change_7d = []
        price = []
        volume_24h = []

        listings = data['data']
        for i in listings:
            coin_name.append(i['name'])
            coin_symbol.append(i['symbol'])
            price.append(i['quote']['USD']['price'])
            percent_change_1h.append(round(i['quote']['USD']['percent_change_1h'], 2))
            percent_change_24h.append(round(i['quote']['USD']['percent_change_24h'], 2))
            percent_change_7d.append(round(i['quote']['USD']['percent_change_7d'], 2))
            market_cap.append(i['quote']['USD']['market_cap'])
            volume_24h.append(i['quote']['USD']['volume_24h'])

        df = pd.DataFrame(
            columns=['coin_name', 'coin_symbol', 'market_cap', 'price', 'percent_change_1h', 'percent_change_24h',
                     'percent_change_7d', 'volume_24h'])
        df['coin_name'] = coin_name
        df['coin_symbol'] = coin_symbol
        df['price'] = price
        df['percent_change_1h'] = percent_change_1h
        df['percent_change_24h'] = percent_change_24h
        df['percent_change_7d'] = percent_change_7d
        df['market_cap'] = market_cap
        df['volume_24h'] = volume_24h
        return df

    def render(self):
        st.title('Crypto Price')

        expander_bar = st.expander("**Выбор криптовалют**")
        expander_bar.markdown("""Источник информации: [CoinMarketCap](http://coinmarketcap.com)""")
        expander_bar.header('Настройка таблицы')

        df = self.load_data()

        sorted_coin = sorted(df['coin_symbol'])
        selected_coin = expander_bar.multiselect('Отображаемые в таблице криптовалюты', sorted_coin, sorted_coin)

        df_selected_coin = df[(df['coin_symbol'].isin(selected_coin))]

        num_coin = expander_bar.slider('Количество отображаемых в таблице криптовалют', 1, 200, 200)  # количество отображаемых криптовалют
        df_coins = df_selected_coin[:num_coin].copy()

        df_coins.rename(columns={
            'coin_symbol': 'symbol',
            'percent_change_1h': '%_ch_1h',
            'percent_change_24h': '%_ch_24h',
            'percent_change_7d': '%_ch_7d',
        }, inplace=True)

        col2 = st.columns(1)[0]
        col2.subheader('Price Data of Selected Cryptocurrency')

        df_coins.loc[:, 'positive_%_change_1h'] = df_coins['%_ch_1h'] > 0
        df_coins.loc[:, 'positive_%_change_24h'] = df_coins['%_ch_24h'] > 0
        df_coins.loc[:, 'positive_%_change_7d'] = df_coins['%_ch_7d'] > 0

        df_coins.index = df_coins.index + 1

        def highlight_positive(val):
            color = '#d4edda' if val else ''
            return f'background-color: {color}'

        styled_df_coins = df_coins.style.format({
            'price': '{:,.2f}',
            'market_cap': '{:,.0f}',
            'volume_24h': '{:,.0f}',
            '%_ch_1h': '{:.2f}',
            '%_ch_24h': '{:.2f}',
            '%_ch_7d': '{:.2f}'
        }).map(highlight_positive, subset=['positive_%_change_1h', 'positive_%_change_24h', 'positive_%_change_7d']) \
            .set_properties(subset=['market_cap', 'volume_24h'], **{'text-align': 'right'})

        table_height = min(35 * (len(df_coins) + 1) + 10, 800)  # Set max height to 800
        col2.dataframe(styled_df_coins, height=table_height)

        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
            href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV File</a>'
            return href

        col2.markdown(filedownload(df_selected_coin), unsafe_allow_html=True)

        # Круговая диаграмма
        stable_symbols = ['USDT', 'USDC', 'FDUSD', 'DAI', 'USDD', 'PYUSD', 'TUSD']
        volume_data = df[['coin_symbol', 'volume_24h']]

        # Вычисляем общую сумму оборота для stable coins и non-stable coins
        stable_volume = volume_data[volume_data['coin_symbol'].isin(stable_symbols)]['volume_24h'].sum()
        non_stable_volume = volume_data[~volume_data['coin_symbol'].isin(stable_symbols)]['volume_24h'].sum()

        # Подготавливаем данные для диаграммы
        labels = ['non-stable coins']
        sizes = [non_stable_volume]
        colors = ['#FF9999']

        for symbol in stable_symbols:
            volume = volume_data[volume_data['coin_symbol'] == symbol]['volume_24h'].sum()
            labels.append(symbol)
            sizes.append(volume)
            colors.append(
                '#66CDAA' if symbol == 'USDT' else
                '#8FBC8F' if symbol == 'USDC' else
                '#20B2AA' if symbol == 'FDUSD' else
                '#B0E57C' if symbol == 'DAI' else
                '#98FB98' if symbol == 'USDD' else
                '#90EE90' if symbol == 'PYUSD' else
                '#8FBC8F' if symbol == 'TUSD' else
                '#B0E57C')

        fig1, ax1 = plt.subplots()
        wedges, texts = ax1.pie(sizes, colors=colors, startangle=90, labels=labels, textprops={'fontsize': 6})
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Добавляем легенду снаружи диаграммы
        legend_labels = [f"{label}: ${size:,.0f}" for label, size in zip(labels, sizes)]
        ax1.legend(wedges, legend_labels, title="Cryptos", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        # Обновляем заголовок диаграммы с объемами
        header_html = f"<h3>Объемы суточного оборота всех non-stable coins (${non_stable_volume:,.0f}) vs stable coins (${stable_volume:,.0f})</h3>"
        st.markdown(header_html, unsafe_allow_html=True)

        st.pyplot(fig1)
