"""
to run locally: streamlit run main.py

1) "Поиск новостей" - Copyright 2024, MS
2) "Биржевые данные" - Copyright 2024, MS
3) "Криптовалюты: цены и объемы" - Copyright 2024, MS
4) "Ипотечный калькулятор" - https://youtu.be/D0D4Pa22iG0?si=3or58vjtabLKvPgf
5) "NBA Player Stats webscraping" - https://youtu.be/JwSS70SZdyM?si=1WLgPMF0noiRbAHU
6) "Uber pickups in NYC, DataSet - 2014" - https://docs.streamlit.io/get-started/tutorials/create-an-app
"""

import streamlit as st
from mortgage_calculator import MortgageCalculator
from news_search import NewsSearch
from stock_data import StockData
from basketball import BasketballStats
from crypto import CryptoData
from uber import UberPickups


class App:
    def __init__(self):
        self.pages = {
            "Поиск новостей": NewsSearch(),
            "Биржевые данные": StockData(),
            "Криптовалюты: цены и объемы": CryptoData(),
            "Ипотечный калькулятор": MortgageCalculator(),
            "NBA Player Stats webscraping": BasketballStats(),
            "Uber Pickups": UberPickups()
        }

    def run(self):
        st.sidebar.title("Приложения")
        page_name = st.sidebar.radio("Выберите:", list(self.pages.keys()))
        page = self.pages[page_name]
        page.render()
        st.sidebar.markdown("<div style='position: fixed; bottom: 0; width: 100%; text-align: left;'>© MS, 2024</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    app = App()
    app.run()
