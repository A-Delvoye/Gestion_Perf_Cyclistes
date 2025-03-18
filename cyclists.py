import sqlite3

# Connexion à la base de données (créée si elle n'existe pas)
conn = sqlite3.connect("cyclists.db")
cursor = conn.cursor()

# Création de la table
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
