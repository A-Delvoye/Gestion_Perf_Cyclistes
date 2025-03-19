import sqlite3
from sqlite3 import Connection

DATABASE_URL = "cyclists.db"

def get_db_connection() -> Connection:
    return sqlite3.connect(DATABASE_URL)
# Connexion à la base de données (créée si elle n'existe pas)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS cyclists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        age INTEGER NOT NULL,
        poids REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        is_active BOOLEAN NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS valid_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expires DATETIME NOT NULL,
        token VARCHAR NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS enregistrements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time DATETIME NOT NULL,
        power REAL NOT NULL,
        oxygen REAL NOT NULL,
        cadence REAL NOT NULL,
        HR REAL NOT NULL,
        RF REAL NOT NULL,
        date DATETIME NOT NULL
    );

    """)
    conn.commit()
    conn.close()

def drop_all_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.executescript("""
    DROP TABLE IF EXISTS cyclists;
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS valid_tokens;
    DROP TABLE IF EXISTS enregistrements;
    DROP TABLE IF EXISTS coachs;
    """)
    conn.commit()
    conn.close()

