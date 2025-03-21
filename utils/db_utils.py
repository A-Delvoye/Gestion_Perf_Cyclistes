import sqlite3

def get_db_connection():
    """
    Établit une connexion à la base de données SQLite.
    """
    conn = sqlite3.connect('db/gest_perf_cycl.db')
    conn.row_factory = sqlite3.Row
    return conn