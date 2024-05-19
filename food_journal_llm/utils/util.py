import os
from dotenv import load_dotenv
import openai


def set_openai_env_vars():
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_KEY")
    os.environ["OPENAI_ORG_ID"] = os.getenv("OPENAI_ORG_ID")
    openai.api_key = os.getenv("OPENAI_API_KEY")


def init_logging():
    import logging
    # save the log to a log file
    logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO)
    return logging.getLogger(__name__)
