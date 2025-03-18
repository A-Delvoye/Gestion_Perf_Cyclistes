import sqlite3

# Connexion à la base de données (créée si elle n'existe pas)
conn = sqlite3.connect("cyclists.db")
cursor = conn.cursor()

# Création de la table cyclists
cursor.execute("""
CREATE TABLE IF NOT EXISTS cyclists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    age INTEGER NOT NULL,
    poids REAL NOT NULL
);
""")

conn.commit()
conn.close()

print("Table 'cyclists' créée avec succès !")





conn = sqlite3.connect("cyclists.db")
cursor = conn.cursor()

cyclistes = [
    ("Julian Alaphilippe", 31, 62.5),
    ("Tadej Pogacar", 25, 66.0),
    ("Jonas Vingegaard", 27, 60.5),
    ("Moi", 33, 152)
]

cursor.executemany("INSERT INTO cyclists (nom, age, poids) VALUES (?, ?, ?)", cyclistes)

conn.commit()
conn.close()

print("Données insérées avec succès !")


#############

# Création des autres tables (users, tokens, coachs, enregistrements)
conn = sqlite3.connect("cyclists.db")
cursor = conn.cursor()
cursor.executescript("""
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
               
CREATE TABLE IF NOT EXISTS Enregistrements (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    time DATETIME NOT NULL, 
    power REAL NOT NULL,
    oxygen REAL NOT NULL,
    cadence REAL NOT NULL,
    HR REAL NOT NULL,
    RF REAL NOT NULL,
    date DATETIME NOT NULL
);
               
CREATE TABLE IF NOT EXISTS Coachs (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nom TEXT NOT NULL, 
    user_id INTEGER NOT NULL, 
    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);
""")

conn.commit()
conn.close()

print("Tables 'users', 'enregistrements', 'Coachs', 'valid_tokens' créées avec succès !")