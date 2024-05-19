import json

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from food_journal_llm.src.retriver import SQLRetriever
from src.utils import mood_to_emoji


class DataframeTableModel:
    def __init__(self, sql_retriever: SQLRetriever):
        self.sql_retriever = sql_retriever

    def get_emoji_mapping(self, df: pd.DataFrame) -> pd.DataFrame:
        df["mood"] = df["mood"].map(mood_to_emoji)
        return df

    def get_last_week_data(self) -> pd.DataFrame:

        # Retive the last week data
        data = self.sql_retriever.retrieve(
            f"SELECT * from table of {st.session_state['username']}. Limit it to 10 entries. Return all the data in the table for the user {st.session_state['username']} as pandas DataFrame. Don't include the username and password columns."
        )
        df = pd.DataFrame(data.metadata["result"], columns=data.metadata["col_keys"])

        return df

    def get_formatted_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.get_emoji_mapping(df)
        df["date"] = pd.to_datetime(df["date"])
        # Format the date
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        # Define the column name mapping
        column_name_mapping = {
            "meal": "Food Item",
            "meal_times": "Meal Time",
            "date": "Date",
            "time": "Time",
            "mood": "Mood",
            "ingredients": "Ingredients",
        }
        # Apply the mapping to the DataFrame
        df = df.rename(columns=column_name_mapping)
        return df

    def render(self):
        df = self.get_last_week_data()
        df = self.get_formatted_data(df)
        st.markdown("## Last week data")
        st.dataframe(df, hide_index=True)


class IngredientsCount:
    def __init__(self, sql_retriever: SQLRetriever):
        self.sql_retriever = sql_retriever

    def get_ingredients_count(self) -> pd.DataFrame:
        data = self.sql_retriever.retrieve(
            f"Return the count of each ingredients for user {st.session_state['username']} SELECT igredients, count(ingredients) from table of {st.session_state['username']} group by ingredients. Return the data as a dictionary with the ingredient as the key and the count as the value."
        )
        # Convert string to dictionary
        # Convert the string representation of list to actual list
        data = [(json.loads(item), count) for item, count in data.metadata["result"]]

        # Flatten the list and create a DataFrame
        df = pd.DataFrame(
            [item for sublist, count in data for item in sublist],
            columns=["Ingredients"],
        )
        df["Count"] = [count for sublist, count in data for item in sublist]
        return df

    def get_transformed_data(self, df: pd.DataFrame) -> pd.DataFrame:
        # Sort the DataFrame by 'Count' in descending order
        df = df.sort_values("Count", ascending=True)
        # Set 'Ingredients' as the index
        df.set_index("Ingredients", inplace=True)
        return df

    def render(self, column: st.delta_generator.DeltaGenerator):
        df = self.get_ingredients_count()
        df = self.get_transformed_data(df)
        column.markdown("## Count of Ingredients")
        column.bar_chart(df)


class MoodPieChart:
    def __init__(self, sql_retriever: SQLRetriever):
        self.sql_retriever = sql_retriever

    def get_mood_data(self) -> pd.DataFrame:
        data = self.sql_retriever.retrieve(
            f"Retrive the mood data for user {st.session_state['username']} Return the data as pandas DataFrame"
        )
        df = pd.DataFrame(data.metadata["result"], columns=data.metadata["col_keys"])
        return df

    def render(self, column: st.delta_generator.DeltaGenerator):
        df = self.get_mood_data()
        labels = df["mood"].unique()
        sizes = df["mood"].value_counts()

        fig1, ax1 = plt.subplots(figsize=(5, 3))
        fig1.patch.set_facecolor("none")  # Make the background transparent
        ax1.pie(
            sizes,
            labels=labels,
            autopct=lambda p: f"{p:.1f}%",
            textprops={"color": "white"},
            shadow=False,
            startangle=90,
        )
        ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
        column.markdown("## Mood data")
        column.pyplot(fig1)
