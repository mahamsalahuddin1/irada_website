import os
import pymysql
from pymysql.cursors import DictCursor

# Load .env if available (optional)
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except Exception:
    pass

def get_db_connection():
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    dbname = os.getenv("DB_NAME", "project_db1")
    return pymysql.connect(
        host=host,
        port=port,
        user=user,
        passwd=password,
        db=dbname,
        cursorclass=DictCursor
    )