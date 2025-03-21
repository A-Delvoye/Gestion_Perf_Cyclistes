import sqlite3
from core.config import DB_NAME


#____________________________________________________________________
# region users
#____________________________________________________________________

# Connexion à la base de données (créée si elle n'existe pas)
with sqlite3.connect(DB_NAME) as conn :
    cursor = conn.cursor()

    # Activer les foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    table_name = "Utilisateurs"
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()

    # Création de la table users
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username VARCHAR NOT NULL, 
            email VARCHAR, 
            password_hash VARCHAR NOT NULL, 
            role VARCHAR NOT NULL
        );
    """)

    conn.commit()
    print(f"Table '{table_name}' créée avec succès !")

#____________________________________________________________________
# region cyclistes
#____________________________________________________________________
with sqlite3.connect(DB_NAME) as conn :
    cursor = conn.cursor()
    # Activer les foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    table_name = "cyclistes"
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()

    # Création de la table cyclistes
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS cyclistes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            age INTEGER NOT NULL,
            poids REAL NOT NULL,
            taille REAL NOT NULL,
            sexe TEXT NOT NULL,
            utilisateur_id INTEGER,
            FOREIGN KEY (utilisateur_id) REFERENCES Utilisateurs(id) ON DELETE CASCADE
        );
        """)    

    conn.commit()
    print(f"Table '{table_name}' créée avec succès !")
    
#____________________________________________________________________
# region enregistrements
#____________________________________________________________________

with sqlite3.connect(DB_NAME) as conn :
    cursor = conn.cursor()
    # Activer les foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")

    table_name = "enregistrements"
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()

    # Création de la table users
    
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS Enregistrements (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            id_utilisateur INTEGER NOT NULL,
            date DATETIME NOT NULL, 
            puissance_max REAL NOT NULL,
            vO2_max REAL NOT NULL,
            cadence_max REAL NOT NULL,
            f_cardiaque_max REAL NOT NULL,
            f_respiratoire_max REAL NOT NULL,
            FOREIGN KEY (id_utilisateur) REFERENCES Utilisateurs(id) ON DELETE CASCADE

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
# region Populate users
#____________________________________________________________________

# Création d'un admin (= coach)
from core.password_tools import get_password_hash
with sqlite3.connect(DB_NAME) as conn :
    cursor = conn.cursor()

    password_hash = get_password_hash("admin")

    admin_values = ("admin", "admin@admin.com", password_hash, "admin")
    
    table_name = "Utilisateurs"
    cursor.execute(f"""
        INSERT INTO {table_name} (username, email, password_hash, role ) 
        VALUES (?, ?, ?, ?) """, admin_values )

    conn.commit()
    print(f"Utilisateur {admin_values[0]} créé succès !")


# Création de users
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
    
    db_session.create_user(db_user)
    count +=1

print(f"{count} UtilisateurDB ajoutés")

#____________________________________________________________________
# region Populate cyclistes
#____________________________________________________________________

# Ajout de cyclistes fictifs
cyclists_data = [
    ("Julian Dupont", 28, 72.5, 1.78, "M"),
    ("Tadej Pogacar", 25, 67.0, 1.76, "M"),
    ("Jonas Vingegaard", 27, 65.0, 1.75, "M"),
    ("Antoine D", 30, 150.0, 1.80, "F"),
    ("Nicolas C", 30, 70.0, 1.79, "M")
]

with sqlite3.connect(DB_NAME) as conn:
    cursor = conn.cursor()
    
    cursor.executemany("""
        INSERT INTO cyclistes (nom, age, poids, taille, sexe) 
        VALUES (?, ?, ?, ?, ?)
    """, cyclists_data)


    # Récupérer tous les utilisateurs (on suppose qu'ils sont ajoutés dans le même ordre que la liste `users`)
    cursor.execute("SELECT id FROM Utilisateurs WHERE role = 'cycliste'")
    utilisateurs_ids = [row[0] for row in cursor.fetchall()]

    # Vérifier que le nombre d'utilisateurs correspond au nombre de cyclistes
    if len(utilisateurs_ids) < len(cyclists_data):
        raise ValueError("Pas assez d'utilisateurs créés pour assigner à chaque cycliste.")

    # Ajout des cyclistes avec un `utilisateur_id`
    cyclists_data_with_id = [
        (nom, age, poids, taille, sexe, utilisateurs_ids[i])
        for i, (nom, age, poids, taille, sexe) in enumerate(cyclists_data)
    ]

    conn.commit()
    print(f"{len(cyclists_data)} cyclistes ajoutés avec succès !")
    print(f"{len(cyclists_data)} cyclistes ajoutés avec succès et liés aux utilisateurs !")
#____________________________________________________________________
# region Populate enregistrements
#____________________________________________________________________

from datetime import datetime
import random

# Génération de données d'enregistrement aléatoires
enregistrements_data = []
for i in range(1, len(cyclists_data)):  # Pour chaque cycliste existant
    for j in range(2):  # 2 enregistrements par cycliste
        enregistrements_data.append((
            i+1,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),  # Date actuelle
            round(random.uniform(200, 500), 2),  # Puissance max (200-500 W)
            round(random.uniform(40, 80), 2),  # VO2 max (40-80 ml/kg/min)
            round(random.uniform(90, 120), 2),  # Cadence max (90-120 rpm)
            round(random.uniform(140, 190), 2),  # Fréquence cardiaque (140-190 bpm)
            round(random.uniform(15, 40), 2)  # Fréquence respiratoire (15-40)
        ))

with sqlite3.connect(DB_NAME) as conn:
    cursor = conn.cursor()

    cursor.executemany("""
        INSERT INTO Enregistrements (id_utilisateur, date, puissance_max, vO2_max, cadence_max, f_cardiaque_max, f_respiratoire_max) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, enregistrements_data)

    conn.commit()
    print(f"{len(enregistrements_data)} enregistrements ajoutés avec succès !")
