"""
to run locally:     streamlit run main.py

1) Поиск по новостным сайтам
Copyright 2024, MS

2) Калькулятор ипотечных процентов - https://youtu.be/D0D4Pa22iG0?si=3or58vjtabLKvPgf
"""
import streamlit as st
from mortgage_calculator import MortgageCalculator
from news_search import NewsSearch

class App:
    def __init__(self):
        self.pages = {
            "Поиск новостей": NewsSearch(),
            "Ипотечный калькулятор": MortgageCalculator()
        }

    def run(self):

        page_name = st.sidebar.radio("", list(self.pages.keys()))
        page = self.pages[page_name]
        page.render()
        st.sidebar.markdown("<div style='position: fixed; bottom: 0; width: 100%; text-align: left;'>© MS, 2024</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    app = App()
    app.run()
