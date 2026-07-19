import os
from dotenv import load_dotenv

load_dotenv()


class MoviesDbCreds:
    DB_MOVIES_HOST=os.getenv("DB_MOVIES_HOST")
    DB_MOVIES_PORT=os.getenv("DB_MOVIES_PORT")
    DB_MOVIES_NAME=os.getenv("DB_MOVIES_NAME")
    DB_MOVIES_USERNAME=os.getenv("DB_MOVIES_USERNAME")
    DB_MOVIES_PASSWORD=os.getenv("DB_MOVIES_PASSWORD")