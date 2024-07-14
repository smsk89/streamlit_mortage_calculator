import yfinance as yf
import streamlit as st
from datetime import date

class StockData:
    def __init__(self):
        pass

    def render(self):
        st.write("""
        # Данные по акциям
        """)

        # Добавляем текстовое поле для ввода тикера
        tickerSymbol = st.text_input("Введите название акции", 'GOOGL')

        # Добавляем ссылку на сайт с названиями акций
        st.markdown('[Список названий акций](https://finance.yahoo.com/lookup/)')

        # Добавляем выбор начальной и конечной даты
        start_date = st.date_input("Выберите начальную дату", date(2010, 1, 1))
        end_date = st.date_input("Выберите конечную дату", date.today())

        # Получаем данные по указанному тикеру
        tickerData = yf.Ticker(tickerSymbol)
        tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

        st.write("""
        ## Closing price, USD
        """)
        if not tickerDf.empty:
            st.line_chart(tickerDf.Close)
        else:
            st.write("Данные отсутствуют.")

        # Получаем рыночную капитализацию
        market_cap = tickerData.info.get('marketCap', 'N/A')

        # Проверяем, что рыночная капитализация не 'N/A' и форматируем с пробелами между разрядами
        if market_cap != 'N/A':
            market_cap = f"{market_cap:,}".replace(',', ' ')

        # Отображаем рыночную капитализацию
        st.write("""
        ## Market capitalization (latest data), USD
        """)
        st.write(market_cap)

        st.write("""
        ## Volume, units
        """)
        if 'Volume' in tickerDf:
            st.line_chart(tickerDf.Volume)
        else:
            st.write("Данные отсутствуют.")

        st.write("""
        ## Dividend, USD
        """)
        if 'Dividends' in tickerDf:
            st.line_chart(tickerDf.Dividends)
        else:
            st.write("Данные отсутствуют.")
