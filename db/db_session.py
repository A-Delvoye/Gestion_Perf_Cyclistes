import sqlite3
from models.utilisateur_db import UtilisateurDB
from models.token_valide_db import TokenValideDB
from datetime import datetime, timezone
from typing import List

class DB_Session() :
    def __init__(self) :
        self.database_path  = "db/gest_perf_cycl.db"
        self.user_tablename = "utilisateurs"
        self.token_tablename = "tokens_valides"

    #__________________________________________________________________________
    #
    # region User
    #__________________________________________________________________________

    def insert_user(self, db_user: UtilisateurDB) :
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

            statement = f"INSERT INTO {self.user_tablename} (username, email, password_hash, role)"
            statement += " VALUES (?, ?, ?, ?);"
            cursor.execute(statement, (db_user.username,  db_user.email, db_user.password_hash, db_user.role))

            number_of_lines = cursor.rowcount     

            connection.commit()

        return True

    def get_user_by_id(self, user_id: int) -> UtilisateurDB:
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()
            cursor.execute(f"SELECT id, username, email, password_hash, role FROM {self.user_tablename} WHERE id = {user_id}")
            rows = cursor.fetchall()

            if rows.count == 1 :
                db_user = self.load_user(rows)
                return UtilisateurDB()
            
        return None

    
    def get_user_list(self) -> List[UtilisateurDB]:
        user_list = list() 
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()
            cursor.execute(f"SELECT id, username, email, password_hash, role FROM {self.user_tablename}")
            rows = cursor.fetchall()

            if rows.count == 0:
                return None

            for row in rows:
                user_list.append(self.load_user(row))

        user_list : List[UtilisateurDB] = user_list

        return user_list 
    
    def get_user_by_name(self, username : str) -> UtilisateurDB:
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()
            cursor.execute(f"SELECT id, username, email, password_hash, role FROM {self.user_tablename} WHERE username = {username}")
            rows = cursor.fetchall()

            if rows.count == 1 :
                db_user = self.load_user(rows)
                return UtilisateurDB()
            
        return None
    
    def load_user(self, row) -> UtilisateurDB :
        db_user = UtilisateurDB(
            id = int(row[0]),
            username= str(row[1]),
            email = str(row[2]),
            password_hash = str(row[3]), 
            role = str(row[4])
        )
        return db_user
    
    #__________________________________________________________________________
    #
    # region Token
    #__________________________________________________________________________

    def insert_token(self, db_token : TokenValideDB) :
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

        return True
    
    def update_token(self, db_token : TokenValideDB) :
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

        return True
    
    def delete_token(self, db_token : TokenValideDB):
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

        return True
    
    def delete_invalid_tokens(self) -> int :
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

            now = datetime.now(timezone.utc)
    
            # for db_token in db_tokens :
            #     expiration = db_token.expires.replace(tzinfo=timezone.utc)
            #     if now > expiration :
            #         db_session.delete(db_token)

        return True 
    
    def get_db_token(self, token : str) -> TokenValideDB:
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

        return TokenValideDB()
    
