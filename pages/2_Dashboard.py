import streamlit as st

from food_journal_llm.src.retriver import SQLRetriever
from src.dashboard_ui import (
    DataframeTableModel,
    IngredientsCount,
    MoodPieChart,
    TimeChart,
)

st.set_page_config(page_title="Dashboard", layout="wide", page_icon="📊")
st.title("📊 Dashboard")
sql_retriever = SQLRetriever(st.session_state["username"], st.session_state["username"])
with st.spinner("Loading your journal..."):
    # Create a DataFrameTableModel object
    dataframe_table_model = DataframeTableModel(sql_retriever)
    dataframe_table_model.render()

with st.spinner("Analysing your journal..."):
    # Create a IngredientsCount object
    ingredients, mood = st.columns(2)

    # Retrieve the count of each ingredient
    ingredients_count = IngredientsCount(sql_retriever)
    ingredients_count.render(ingredients)

    # Retrieve the mood data
    mood_pie_chart = MoodPieChart(sql_retriever)
    mood_pie_chart.render(mood)

    # Retrive the time split data
    time_chart = TimeChart(sql_retriever)
    time_chart.render()
