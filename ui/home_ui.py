import json

import streamlit as st

from food_journal_llm.src.retriver import SQLRetriever
from food_journal_llm.src.vision import analyse_image


class IngredientAnalyser:
    def __init__(self, sql_retriever: SQLRetriever):
        self.sql_retriever = sql_retriever

    def file_uploader(self):

        image_response = st.file_uploader(
            "Upload a photo of your food", type=["jpg", "jpeg", "png"]
        )
        return image_response

    def save_image(self, image_response):
        if image_response:
            with open("upload.jpg", "wb") as f:
                f.write(image_response.read())
            return "upload.jpg"
        else:
            return None

    @st.cache_data(show_spinner="Analysing the image...")
    def analyse_image(_self, image_path):
        if image_path is not None:
            ingredients = analyse_image(image_path)
            return ingredients
        else:
            return None

    def render(self):
        st.markdown("#### Analyse the ingredients of your food")
        image_response = self.file_uploader()
        image_path = self.save_image(image_response)
        ingredients_string = self.analyse_image(image_path)
        if image_response is not None:
            # Parse the JSON string
            ingredients_list = json.loads(ingredients_string)
        else:
            ingredients_list = None
        if ingredients_list is not None:
            ingredients_list_str = ", ".join(ingredients_list["ingredients"])
            st.markdown(f"The ingredients in your food are: {ingredients_list_str}")
        return ingredients_list


class FoodJournal:
    def __init__(self, sql_retriever: SQLRetriever):
        self.sql_retriever = sql_retriever

    def get_ingredients(self, ingredients):
        ingredients_only = ingredients["ingredients"]
        # make the list of ingredients into a string
        ingredients_only = ", ".join(ingredients_only)
        return ingredients_only

    def render(self, ingredients: dict):
        food = st.text_input("What did you eat?", "Dosa with tomato chutney")
        meal_cat = st.selectbox(
            "Meal of the day", ["Breakfast", "Lunch", "Dinner", "Snack"]
        )
        date = st.date_input("Date eaten", value=None, min_value=None, max_value=None)
        time = st.time_input("Time eaten", value=None)
        if ingredients is not None:
            try:
                ingredients_only = self.get_ingredients(ingredients)
            except Exception as e:
                # Handle the error
                print(f"An error occurred while getting the ingredients: {e}")
        else:
            ingredients_only = "Dosa, tomato, chutney"

        ingredients_entry = st.text_area("Ingredients", ingredients_only)

        after_eating = st.selectbox(
            "How do you feel after eating?",
            [
                "Happy",
                "Sad",
                "Neutral",
                "Bloated",
                "Satisfied",
                "Hungry",
                "Burpy",
                "Thirsty",
                "Full",
                "Tired",
                "Energetic",
                "Sick",
                "Nauseous",
                "Gassy",
                "Constipated",
                "Diarrhea",
                "Heartburn",
                "Acid Reflux",
                "Other",
            ],
        )
        submit = st.button("Submit")

        jounral_entry = {
            "food": food,
            "meal_cat": meal_cat,
            "date": date,
            "time": time,
            "ingredients": ingredients_entry,
            "after_eating": after_eating,
        }
        return jounral_entry, submit
