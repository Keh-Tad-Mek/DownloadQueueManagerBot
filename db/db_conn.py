import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("DATABASE_URL")

if not url:
    raise ValueError("DATABASE_URL environment variable is not set.")


def get_connection():
    return psycopg.connect(url)