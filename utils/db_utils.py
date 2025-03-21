import sqlite3
from core.config import DB_NAME
def get_db_connection():
    """
    Établit une connexion à la base de données SQLite.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn