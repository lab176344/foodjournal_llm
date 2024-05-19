import streamlit as st
import streamlit_authenticator as stauth  # type: ignore
import yaml  # type: ignore
from yaml.loader import SafeLoader  # type: ignore

from food_journal_llm.src.retriver import SQLRetriever
from src.home_ui import FoodJournal, IngredientAnalyser

# Have a signup and login page
# use two buttons to switch between the two
with open("config/config.yaml", "r") as f:
    config = yaml.load(f, Loader=SafeLoader)
st.set_page_config(
    page_title="Food Journal LLM", layout="wide", page_icon=":fork_and_knife:"
)
st.title("Food Journal LLM")
navigation = ["Login", "Signup"]
option = st.sidebar.selectbox("Navigation", navigation)
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["pre-authorized"],
)

if option == "Login":
    authenticator.login()
    if st.session_state["authentication_status"]:
        username = st.session_state["username"]
        st.write(f"Welcome {username}")
        use_ingredients = False
        sql_retriever = SQLRetriever(username, username)
        ingredient_analyser = IngredientAnalyser(sql_retriever)
        ingredients = ingredient_analyser.render()
        food_journal = FoodJournal(sql_retriever)
        journal_entry, submit = food_journal.render(ingredients=ingredients)
        food = journal_entry["food"]
        meal_cat = journal_entry["meal_cat"]
        date = journal_entry["date"]
        time = journal_entry["time"]
        after_eating = journal_entry["after_eating"]
        if submit:

            table_name = "food_journal_user_" + username
            prompt = f"insert into {table_name} in the same order (username, password, meal, meal_times, date, time, mood, ingredients) values ('{username}', {username}, '{food}', '{meal_cat}', '{date}', '{time}', '{after_eating}', ' {ingredients}')"  # noqa E501
            response = sql_retriever.insert(prompt)
            response_content = response.response
            if (
                "inserted" in response_content
                or "updated" in response_content
                or "successful" in response_content
                or "successfully" in response_content
            ):
                st.info("Your entry is recorded")
            else:
                st.info("Try again later")
    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")
        authenticator.logout(location="sidebar")

elif option == "Signup":
    try:
        (
            email_of_registered_user,
            username_of_registered_user,
            name_of_registered_user,
        ) = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            st.success("User registered successfully")
        with open("config/config.yaml", "w") as file:
            yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)
