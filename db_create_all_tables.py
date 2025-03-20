import sqlite3

#____________________________________________________________________
# region users
#____________________________________________________________________

# Connexion à la base de données (créée si elle n'existe pas)
with sqlite3.connect("db/gest_perf_cycl.db") as conn :
    cursor = conn.cursor()

    table_name = "utilisateurs"
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()

    # Création de la table users
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER NOT NULL, 
            username VARCHAR NOT NULL, 
            email VARCHAR, 
            password_hash VARCHAR NOT NULL, 
            role VARCHAR NOT NULL, 
            PRIMARY KEY (id)
        );
    """)

    conn.commit()
    print(f"Table '{table_name}' créée avec succès !")

#____________________________________________________________________
# region cyclistes
#____________________________________________________________________
with sqlite3.connect("db/gest_perf_cycl.db") as conn :
    cursor = conn.cursor()

    table_name = "cyclistes"
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()

    # Création de la table users
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS cyclists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            age INTEGER NOT NULL,
            poids REAL NOT NULL,
            taille REAL NOT NULL,
            sexe TEXT NOT NULL
        );
        """)    

    conn.commit()
    print(f"Table '{table_name}' créée avec succès !")
    
#____________________________________________________________________
# region enregistrements
#____________________________________________________________________

with sqlite3.connect("db/gest_perf_cycl.db") as conn :
    cursor = conn.cursor()

    table_name = "enregistrements"
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()

    # Création de la table users
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Enregistrements (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            date DATETIME NOT NULL, 
            puissance_max REAL NOT NULL,
            v02_max REAL NOT NULL,
            cadence_max REAL NOT NULL,
            f_cardiaque REAL NOT NULL,
            f_respiratoire REAL NOT NULL,
            date DATETIME NOT NULL
        );
        """)    

    conn.commit()
    print(f"Table '{table_name}' créée avec succès !")

#____________________________________________________________________
# region jetons_valides
#____________________________________________________________________

    table_name = "jetons_valides"
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()

    # Création de la table token 
    cursor.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER NOT NULL, 
            expiration DATETIME NOT NULL, 
            jeton VARCHAR NOT NULL, 
            PRIMARY KEY (id)
        );
    """)

    conn.commit()
    print(f"Table '{table_name}' créée avec succès !")

#____________________________________________________________________
# Populate users
#____________________________________________________________________

# Création d'un admin (= coach)
from core.password_tools import get_password_hash
with sqlite3.connect("db/gest_perf_cycl.db") as conn :
    cursor = conn.cursor()

    password_hash = get_password_hash("admin")

    admin_values = ("admin", "admin@admin.com", password_hash, "admin")
    
    table_name = "Utilisateurs"
    cursor.execute(f"""
        INSERT INTO {table_name} (username, email, password_hash, role ) 
        VALUES (?, ?, ?, ?) """, admin_values )

    conn.commit()
    print(f"Utilisateur {admin_values[0]} créé succès !")


# Création de cyclistes
from db.db_session import DB_Session
from models.utilisateur_db import UtilisateurDB

from core.password_tools import get_password_hash

db_session = DB_Session()

users = [ 
    ("Julian Dupont", "jul@yan.com", get_password_hash("Julian")),
    ("Tadej", "tad@ej.com", get_password_hash("Tadej")),
    ("Jonas", "jon@as.com", get_password_hash("Jonas")),
    ("Antoine", "ant@oine.com", get_password_hash("Antoine")),
    ("Nicolas", "nic@olas.com", get_password_hash("Nicolas"))]

count=0
for user in users :
    db_user = UtilisateurDB(
        username = user[0], 
        email = user[1],
        password_hash=user[2], 
        role = str("cycliste"))
    
    db_session.insert_user(db_user)
    count +=1

print(f"{count} UtilisateurDB ajoutés")