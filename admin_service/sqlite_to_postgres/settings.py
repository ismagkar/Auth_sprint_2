import logging
import os

from dotenv import load_dotenv

load_dotenv()

DSN_PSQL = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
}

SQLITE_DB_PATH = os.environ.get("SQLITE_DB_PATH", ":memory:")

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=os.environ.get("LOG_LEVEL", "DEBUG"))
