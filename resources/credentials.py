import os
from dotenv import load_dotenv

load_dotenv()


class MoviesCreds:
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

    SUPER_ADMIN_USERNAME = os.getenv("SUPER_ADMIN_USERNAME")
    SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")