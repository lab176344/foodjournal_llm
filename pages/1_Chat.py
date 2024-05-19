import streamlit as st

from food_journal_llm.src.retriver import SQLRetriever

st.set_page_config(page_title="Food GPT", layout="wide", page_icon="📄")

st.title("🍽️ FoodGPT 📄")
response_table = ""


@st.cache_resource
def get_sql_retriever(username):
    return SQLRetriever(username, username)


@st.cache_data(show_spinner="Fetching data...")
def get_data(_sql_retriever: SQLRetriever, username: str):
    # Display chat messages from history on app rerun
    prompt_table = f"""SELECT * FROM the table name of the database for the user {username} for the last 60 days. Dont include the username and password columns. Return the data in a parsable format."""
    response_table = str(_sql_retriever.get_table_data(prompt_table))
    return response_table


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

sql_retriever: SQLRetriever = get_sql_retriever(st.session_state["username"])

if not len(response_table) > 0:
    response_table += get_data(sql_retriever, st.session_state["username"])

max_length = 128000
# Accept user input
if prompt := st.chat_input("Explore your Journal"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
        # Display assistant response in chat message container
    with st.spinner("Analysing your journal..."):
        with st.chat_message("assistant"):
            response = str(sql_retriever.chat(prompt, response_table))
            st.markdown(response)
        # Add the last generated message to the response table
        response_table = response_table[:max_length]
        response_table += response
        st.session_state.messages.append({"role": "assistant", "content": response})
