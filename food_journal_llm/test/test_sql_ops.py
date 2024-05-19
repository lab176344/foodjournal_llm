from llama_index.core.utilities.sql_wrapper import SQLDatabase
from sqlalchemy import insert, delete
from food_journal_llm.src.database import FoodJournalUser
from food_journal_llm.src.prompt import n_gram_nouns_adjectives
from food_journal_llm.src.retriver import SQLRetriever
import pytest
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random
import json

ingredients = ['rice', 'wheat', 'milk', 'egg', 'mango', 'banana', 'apple', 'orange', 'grapes', 'chicken', 'beef', 'pork', 'carrot', 'potato', 'tomato', 'lettuce', 'cabbage', 'spinach', 'broccoli', 'peas', 'beans', 'corn', 'pepper', 'onion', 'garlic', 'ginger', 'turmeric', 'cumin', 'coriander', 'cardamom', 'cinnamon', 'nutmeg', 'vanilla', 'chocolate', 'sugar', 'salt', 'pepper', 'vinegar', 'soy sauce', 'olive oil', 'butter', 'cheese', 'yogurt', 'cream', 'pasta', 'bread', 'flour', 'yeast', 'baking powder', 'baking soda', 'cocoa powder', 'honey', 'jam', 'jelly', 'syrup', 'ketchup', 'mayonnaise', 'mustard', 'pickles', 'relish', 'salsa', 'chutney', 'sauce', 'gravy', 'soup', 'stew', 'curry', 'salad', 'sandwich', 'burger', 'pizza', 'taco', 'burrito', 'quesadilla', 'sushi', 'sashimi', 'nigiri', 'maki', 'temaki', 'ramen', 'pho', 'pad thai', 'samosa', 'spring roll',
               'dumpling', 'empanada', 'pierogi', 'poutine', 'pasta', 'lasagna', 'ravioli', 'gnocchi', 'cannelloni', 'risotto', 'paella', 'couscous', 'tagine', 'kebab', 'shawarma', 'tandoori', 'satay', 'kabob', 'gyro', 'souvlaki', 'tikka', 'masala', 'korma', 'vindaloo', 'saag', 'paneer', 'dal', 'biryani', 'pulao', 'kheer', 'ladoo', 'jalebi', 'gulab jamun', 'rasgulla', 'barfi', 'halwa', 'kulfi', 'lassi', 'chai', 'coffee', 'tea', 'juice', 'smoothie', 'shake', 'soda', 'water', 'milkshake', 'cocktail', 'mocktail', 'beer', 'wine', 'whiskey', 'vodka', 'rum', 'gin', 'tequila', 'brandy', 'liqueur', 'champagne', 'sake', 'soju', 'baijiu', 'shochu', 'arak', 'ouzo', 'absinthe', 'vermouth', 'amaretto', 'kahlua', 'baileys', 'cointreau', 'triple sec', 'grand marnier', 'campari', 'aperol', 'chartreuse', 'benedictine', 'frangelico', 'galliano', 'sambuca', 'jagermeister', 'fireball',]


meals = ['pasta', 'chicken curry', 'pizza', 'sushi', 'hamburger', 'lasagna', 'tacos', 'steak', 'salmon', 'fried rice', 'spaghetti', 'pad thai', 'samosa', 'pancakes', 'burrito', 'gnocchi', 'ramen', 'grilled cheese sandwich', 'mashed potatoes', 'falafel', 'quesadilla', 'biryani', 'omelette', 'pho', 'beef stew', 'lobster', 'shrimp scampi', 'enchiladas', 'chow mein', 'chili', 'risotto', 'chicken wings', 'sashimi', 'hot dog', 'chicken salad', 'calamari', 'croissant', 'crab cakes', 'spring rolls', 'macaroni and cheese', 'ratatouille', 'paella', 'cannoli', 'fajitas', 'ceviche', 'tiramisu', 'clam chowder', 'lobster bisque', 'stir fry', 'sloppy joes', 'gyro', 'caesar salad', 'bruschetta', 'scones', 'lobster roll',
         'chicken parmesan', 'waffles', 's\'mores', 'cobb salad', 'cinnamon rolls', 'philly cheesesteak', 'hummus', 'caprese salad', 'quiche', 'tandoori chicken', 'gumbo', 'carbonara', 'pad see ew', 'bagel with lox', 'moussaka', 'poutine', 'baba ganoush', 'schnitzel', 'bibimbap', 'churros', 'chicken tikka masala', 'tempura', 'peking duck', 'empanadas', 'lobster mac and cheese', 'miso soup', 'corned beef hash', 'deviled eggs', 'beef Wellington', 'crème brûlée', 'falafel wrap', 'sweet and sour chicken', 'eggplant parmesan', 'chicken katsu', 'french toast', 'chocolate fondue', 'beef bourguignon', 'sushi burrito', 'croque monsieur', 'beef bulgogi', 'dumplings', 'bánh mì', 'frittata', 'fish and chips', 'beef brisket']


meal_times = ['breakfast', 'lunch', 'dinner', 'snack']


@ pytest.fixture
def dummy_data() -> List[Dict[str, Any]]:
    return [
        {
            'id': i,
            'username': 'lakshmanb',
            'password': 'lakshmanb',
            'meal': random.choice(meals),
            'meal_times': random.choice(meal_times),
            'date': (datetime.now() - timedelta(days=i)).date(),
            'time': (datetime.now() - timedelta(hours=random.randint(6, 19))).time().strftime('%H:%M:%S'),
            'mood': 'Happy' if i % 2 == 0 else 'Sad',
            # Convert list to string
            'ingredients': json.dumps([random.choice(ingredients) for _ in range(3)])
        }
        for i in range(1, 100)  # Generate 1000 rows of data
        # Add more dummy data as needed
    ]


@ pytest.fixture
def user_creation():
    username = 'lakshmanb'
    password = 'lakshmanb'
    return username, password


def test_sql_insertion(dummy_data, user_creation):
    username = user_creation[0]
    password = user_creation[1]
    user = FoodJournalUser(username, password)
    sql_database = SQLDatabase(user.engine,
                               include_tables=[user.table_name])

    # Clear the table before inserting data
    delete_stmt = delete(user.table)
    with user.engine.begin() as conn:
        conn.execute(delete_stmt)

    for data in dummy_data:
        stmt = insert(user.table).values(**data)
        with user.engine.begin() as conn:
            conn.execute(stmt)
    table_names = sql_database.get_usable_table_names()

    assert user.table_name in table_names


def test_n_gram_nouns_adjectives():
    text = "I am eating a delicious pizza"
    n_grams_nouns, n_gram_adjectives = n_gram_nouns_adjectives(text, n=2)
    assert n_grams_nouns == [('pizza')]
    assert n_gram_adjectives == [('delicious')]


def test_sql_insertion_query(user_creation):
    user = "user1"
    meal = "avocado burger"
    meal_type = "lunch"
    mood = "bloated"
    date = datetime(2022, 1, 1)
    time = datetime(2022, 1, 1, 12, 0, 0)
    prompt_insert = f"The {user} ate {meal} for {meal_type} on {date} at {time} and felt {mood}. Insert this into the table please. Correct the spelling mistakes if any."
    retriever = SQLRetriever(user_creation[0], user_creation[1])
    response = retriever.insert(prompt_insert)
    assert "successfully inserted" in str(response)
    prompt_retrive = f"Get what did the {user} eat when {user}'s mood was {mood}."
    response = retriever.insert(prompt_retrive)
    assert meal in str(response)
    prompt_retrive = f"Get how many times {user} felt {mood}."
    assert "one" or "1" in str(response)
