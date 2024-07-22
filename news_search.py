import requests
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
import os


class NewsSearch:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("NEWS_API_KEY")

    def get_news(self, search, amount):
        response = requests.get(
            f"https://newsapi.org/v2/everything?q={search}&apiKey={self.api_key}&pageSize={amount}")
        data = response.json()
        mrgn = 20

        if data['status'] == 'ok' and data['totalResults'] > 0:
            articles = sorted(data['articles'], key=lambda x: x['publishedAt'], reverse=True)
            n = 1
            for article in articles:
                date = datetime.strptime(article['publishedAt'], "%Y-%m-%dT%H:%M:%SZ").strftime("%d.%m.%Y")
                title = article['title']
                description = article['description']
                source_name = article['source']['name']
                url = article['url']

                st.markdown(f'<br><p><strong>{n}) {title}</strong></p>', unsafe_allow_html=True)
                st.markdown(f'<p style="margin-left: {mrgn}px; color: #BDBDBD;">{date}</p>', unsafe_allow_html=True)
                if description:
                    description = description.replace('\n', '<br>').replace('\r', '<br>')
                    st.markdown(f'<p style="margin-left: {mrgn}px; color: #BDBDBD;">{description}</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="margin-left: {mrgn}px; color: #BDBDBD;"><strong>Источник:</strong> {source_name}</p>', unsafe_allow_html=True)
                st.markdown(f'<p style="margin-left: {mrgn}px;"><a href="{url}" target="_blank" style="color: #BDBDBD;">{url}</a></p>', unsafe_allow_html=True)
                n += 1

        else:
            st.write("За последние 30 дней не было новостей по этой теме.")

    def render(self):
        st.title("Поиск информации")
        st.markdown('<p style="font-size: 20px;">по 150 000 новостным сайтам (за последние 30 дней)</p>', unsafe_allow_html=True)
        question = st.text_input("Поисковый запрос:")
        answer_amount = st.number_input("Какое максимальное количество новостей показать:", min_value=1, step=1)

        if st.button("Получить новости"):
            self.get_news(question, answer_amount)
