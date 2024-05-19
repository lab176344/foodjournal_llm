from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.core.objects import (
    SQLTableNodeMapping,
    ObjectIndex,
    SQLTableSchema,
)
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import (
    SQLTableRetrieverQueryEngine,
)
from datetime import datetime
from food_journal_llm.src.database import FoodJournalUser
from llama_index.core.utilities.sql_wrapper import SQLDatabase
from food_journal_llm.utils.util import set_openai_env_vars


class SQLRetriever:
    """
    A class that provides methods for retrieving and inserting data into an SQL database.

    Args:
        user_name (str): The username for accessing the SQL database.
        password (str): The password for accessing the SQL database.

    Attributes:
        user_name (str): The username for accessing the SQL database.
        password (str): The password for accessing the SQL database.
        query_engine (SQLTableRetrieverQueryEngine): The query engine for executing SQL queries.

    Methods:
        retrieve(query: str) -> Any: Retrieves data from the SQL database based on the given query.
        insert(data: str) -> Any: Inserts data into the SQL database.

    """

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
        set_openai_env_vars()
        user = FoodJournalUser(user_name, password)
        sql_database = SQLDatabase(user.engine,
                                   include_tables=[user.table_name])
        self.table_name = user.table_name
        # manually set context text
        table_stat_text = (
            "This table gives information regarding meal eaten by each user"
            "The columns in the table include the meal, type of meal, date and time of the meal, mood of the user, ingredients of the meal,"
            f" along with how they felt after eating the meal. Today's date is {datetime.now().date()}."
        )
        llm = OpenAI(temperature=0.1, model="gpt-4-turbo")
        # set Logging to DEBUG for more detailed outputs
        table_node_mapping = SQLTableNodeMapping(sql_database)
        table_schema_objs = [
            (SQLTableSchema(table_name=user.table_name, context_str=table_stat_text)
             )
        ]  # add a SQLTableSchema for each table

        obj_index = ObjectIndex.from_objects(
            table_schema_objs,
            table_node_mapping,
            VectorStoreIndex,
        )
        self.query_engine = SQLTableRetrieverQueryEngine(
            table_retriever=obj_index.as_retriever(similarity_top_k=5),
            llm=llm,
            sql_database=sql_database
        )

    def retrieve(self, query: str):
        """
        Retrieves data from the SQL database based on the given query.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            Any: The result of the query execution.

        """
        assert isinstance(query, str)
        query = """This is a query to retrieve data from the SQL database. The schema of the table, table = Table(
            self.table_name,
            self.metadata,
            Column('id', Integer),
            Column('username', String),
            Column('password', String),
            Column('meal', String),
            Column('meal_times', String),
            Column('date', DateTime),
            Column('time', String),
            Column('mood', String),
            Column('ingredients', String),
            PrimaryKeyConstraint('id'),
        )""" + "The retrival query is: " + query + "Don't add any thing related to SQL in the response. Make it sound like a human response. If addessing the user, use 'you' instead of 'the user'. Don't add any SQL keywords in the response."
        return self.query_engine.query(query)

    def get_table_data(self, query: str):
        """
        Retrieves data from the SQL database based on the given query.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            Any: The result of the query execution.

        """
        assert isinstance(query, str)
        query = """This is a query to retrieve data from the SQL database. The schema of the table, table = Table(
            self.table_name,
            self.metadata,
            Column('id', Integer),
            Column('username', String),
            Column('password', String),
            Column('meal', String),
            Column('meal_times', String),
            Column('date', DateTime),
            Column('time', String),
            Column('mood', String),
            Column('ingredients', String),
            PrimaryKeyConstraint('id'),
        )""" + "The retrival query is: " + query
        return self.query_engine.query(query)

    def chat(self, query: str, response_table: str):
        """
        Chats with the data from the SQL database based on the given query.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            Any: The result of the query execution.

        """

        assert isinstance(query, str)

        prompt = f"""Given the table information: {response_table}. Answer the following question: {query}. Dont't add any SQL keywords in the response. Make it sound like a human response. If addessing the user, use 'you' instead of 'the user'."""
        return self.query_engine.query(prompt)

    def insert(self, data: str):
        """
        Inserts data into the SQL database.

        Args:
            data (str): The SQL query for inserting data into the database.

        Returns:
            Any: The result of the query execution.

        """
        assert isinstance(data, str)
        data = """This is a query to insert data into the SQL database. The schema of the table, table = Table(
            self.table_name,
            self.metadata,
            Column('id', Integer),
            Column('username', String),
            Column('password', String),
            Column('meal', String),
            Column('meal_times', String),
            Column('date', DateTime),
            Column('time', String),
            Column('mood', String),
            Column('ingredients', String),
            PrimaryKeyConstraint('id'),
        )""" + "The insert query is: " + data
        return self.query_engine.query(data)
