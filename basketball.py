import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


@st.cache_data
def load_data(_year):
    url = f"https://www.basketball-reference.com/leagues/NBA_{_year}_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)

    # Преобразование всех процентных столбцов в числовой формат
    percentage_columns = ['FG%', '3P%', '2P%', 'eFG%', 'FT%']
    for col in percentage_columns:
        playerstats[col] = pd.to_numeric(playerstats[col], errors='coerce').fillna(0)

    return playerstats


class BasketballStats:
    def __init__(self):
        pass

    def filedownload(self, df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
        return href

    def render(self):
        st.title('NBA Player Stats')

        st.markdown("""
        **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/)
        """)

        right_sidebar = st.expander("User Input Features", expanded=True)
        with right_sidebar:
            selected_year = st.selectbox('Year', list(reversed(range(1950, 2024))))

        playerstats = load_data(selected_year)

        with right_sidebar:
            sorted_unique_team = sorted(playerstats.Tm.unique())
            selected_team = st.multiselect('Team', sorted_unique_team, sorted_unique_team)

            unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
            selected_pos = st.multiselect('Position', unique_pos, unique_pos)

        df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

        st.header('Display Player Stats of Selected Team(s)')
        st.write(f'Data Dimension: {df_selected_team.shape[0]} rows and {df_selected_team.shape[1]} columns.')
        st.dataframe(df_selected_team)

        st.markdown(self.filedownload(df_selected_team), unsafe_allow_html=True)

        if st.button('Intercorrelation Heatmap'):
            st.header('Intercorrelation Matrix Heatmap')
            df_selected_team.to_csv('output.csv', index=False)
            df = pd.read_csv('output.csv')

            numeric_df = df.select_dtypes(include=[np.number])

            corr = numeric_df.corr()
            mask = np.zeros_like(corr)
            mask[np.triu_indices_from(mask)] = True
            with sns.axes_style("white"):
                f, ax = plt.subplots(figsize=(7, 5))
                ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
            st.pyplot(f)
