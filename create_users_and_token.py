import sqlite3

# Connexion à la base de données (créée si elle n'existe pas)
with sqlite3.connect("db/gest_perf_cycl.db") as conn :
    cursor = conn.cursor()

    # Création de la table user
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER NOT NULL, 
            username VARCHAR NOT NULL, 
            email VARCHAR, 
            password_hash VARCHAR NOT NULL, 
            role VARCHAR NOT NULL, 
            is_active BOOLEAN NOT NULL, 
            PRIMARY KEY (id)
        );
    """)

    conn.commit()
    print("Table 'user' créée avec succès !")

    # Création de la table token 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS valid_token (
            id INTEGER NOT NULL, 
            expires DATETIME NOT NULL, 
            token VARCHAR NOT NULL, 
            PRIMARY KEY (id)
        );
    """)

    conn.commit()
    print("Table 'valid_token' créée avec succès !")

    password_hash = "Azerty123"

    admin = ("admin", "admin@admin.com", password_hash, "admin", "1")
    
    cursor.execute("""
        INSERT INTO user (username, email, password_hash, role, is_active ) 
        VALUES (?, ?, ?, ?, ?) """, admin)

    conn.commit()
    print("User Admin créé succès !")


