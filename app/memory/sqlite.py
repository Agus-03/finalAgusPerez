import sqlite3
from app.config import SQLITE_DB

def get_conn():
    return sqlite3.connect(SQLITE_DB)
