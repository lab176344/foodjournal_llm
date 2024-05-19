from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    DateTime,
    PrimaryKeyConstraint,
    select,
    inspect)
from sqlalchemy.exc import SQLAlchemyError
from food_journal_llm.utils.util import init_logging


class FoodJournalUser():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.table_name = 'food_journal_user_' +\
            self.username
        self.engine = create_engine('sqlite:///food_journal.db')
        self.metadata = MetaData()
        self.table = self._get_table_schema()
        self.logger = init_logging()

    def _get_table_schema(self) -> Table:
        table = Table(
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
        )
        try:
            inspector = inspect(self.engine)
            if not inspector.has_table(self.table_name):
                self.metadata.create_all(self.engine)
        except SQLAlchemyError as e:
            self.logger.error(f"Error creating table {self.table_name}: {e}")

        return table

    def get_table_data(self, table_name):
        # Get the Table object
        # Assuming _get_table is a method that returns a Table object
        table = self._get_table(table_name)

        if table is None:
            raise ValueError(f"Table {table_name} does not exist")

        # Create a SELECT statement
        stmt = select(table)

        # Execute the statement and fetch all rows
        with self.engine.connect() as connection:
            result = connection.execute(stmt).fetchall()

        return result
