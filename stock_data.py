import yfinance as yf
import streamlit as st
from datetime import date

class StockData:
    def __init__(self):
        pass

    def render(self):
        st.write("""
        # Биржевые данные
        """)

        if 'selected_ticker' not in st.session_state:
            st.session_state.selected_ticker = 'GOOGL'

        with st.expander("Выбор данных", expanded=True):
            # Добавляем текстовое поле для ввода тикера
            tickerSymbol = st.text_input("Введите название:", st.session_state.selected_ticker)

            # Добавляем ссылку на сайт с названиями акций
            st.markdown('[Список всех названий](https://finance.yahoo.com/lookup/)')

            # Добавляем поле с популярными активами
            st.write("Популярные:")
            popular_assets = {
                "GOOGL": "Alphabet Inc.",
                "AAPL": "Apple Inc.",
                "^DJI": "Dow Jones Ind.",
                "BTC-USD": "Bitcoin USD",
                "GC=F": "Золото"
            }

            # Создаем колонки для популярных активов
            cols = st.columns(len(popular_assets))
            for col, (symbol, name) in zip(cols, popular_assets.items()):
                if col.button(f"{symbol}"):
                    st.session_state.selected_ticker = symbol
                    st.rerun()
                col.write(f"{name}")

            # Добавляем выбор начальной и конечной даты
            start_date = st.date_input("Выберите начальную дату", date(2010, 1, 1))
            end_date = st.date_input("Выберите конечную дату", date.today())

        # Получаем данные по указанному тикеру
        tickerData = yf.Ticker(tickerSymbol)
        tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

        # Получаем последнее значение закрытия и округляем его до 2 знаков
        last_close = round(tickerDf['Close'].iloc[-1], 2) if not tickerDf.empty else 'N/A'

        # Отображаем название актива
        asset_name = tickerData.info.get('longName', 'N/A')
        st.write(f"""
        ## {asset_name} ({tickerSymbol})
        """)

        st.write(f"""
        ### Closing price, USD {last_close}
        """)
        if not tickerDf.empty:
            st.line_chart(tickerDf.Close)
        else:
            st.write("Данные отсутствуют.")

        # Получаем рыночную капитализацию
        market_cap = tickerData.info.get('marketCap', 'N/A')

        # Проверяем, что рыночная капитализация не 'N/A' и форматируем с пробелами между разрядами
        if market_cap != 'N/A':
            market_cap = f"{int(market_cap):,}".replace(',', ' ')

        # Отображаем рыночную капитализацию
        st.write(f"""
        ### Market capitalization (latest data), USD {market_cap}
        """)

        st.write("""
        ### Volume, units
        """)
        if 'Volume' in tickerDf:
            st.line_chart(tickerDf.Volume)
        else:
            st.write("Данные отсутствуют.")

        st.write("""
        ### Dividend, USD
        """)
        if 'Dividends' in tickerDf:
            st.line_chart(tickerDf.Dividends)
        else:
            st.write("Данные отсутствуют.")
