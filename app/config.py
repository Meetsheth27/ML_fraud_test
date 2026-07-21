import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Application Configuration
    """

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    CHANNEL_NAME = os.getenv("CHANNEL_NAME")

    MODEL_PATH = os.getenv("MODEL_PATH")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")