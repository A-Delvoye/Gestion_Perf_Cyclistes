import sqlite3
from models.utilisateur_db import UtilisateurDB
from models.jeton_valide_db import JetonValideDB
from datetime import datetime, timezone
from typing import List

class DB_Session() :
    def __init__(self) :
        self.database_path  = "db/gest_perf_cycl.db"
        self.user_tablename = "utilisateurs"
        self.token_tablename = "jetons_valides"
        self.date_format_string = "%Y-%m-%d %H:%M:%S.%f"

    #__________________________________________________________________________
    #
    # region Utilisateur
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
            result = cursor.fetchone()

            if result :
                db_user = self.load_user(result)
                return db_user
            
        return None

    
    def get_user_list(self) -> List[UtilisateurDB]:
        user_list = list() 
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

            statement  = f"SELECT id, username, email, password_hash, role"
            statement +=f" FROM {self.user_tablename}"
  
            cursor.execute(statement)
            rows = cursor.fetchall()

            if len(rows) == 0:
                return None

            for row in rows:
                user_list.append(self.load_user(row))

        user_list : List[UtilisateurDB] = user_list

        return user_list 
    
    def get_user_by_name(self, username : str) -> UtilisateurDB:
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

            statement  = "SELECT id, username, email, password_hash, role"
            statement +=f" FROM {self.user_tablename}"
            statement +=f" WHERE username = '{username}'"
    
            cursor.execute(statement)
            result = cursor.fetchone()

            if result :
                db_user = self.load_user(result)
                return db_user
            
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
    # region Jeton 
    #__________________________________________________________________________

    
    def insert_token(self, db_token : JetonValideDB) :
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

            date_str = db_token.expiration.strftime(self.date_format_string)

            statement = f"INSERT INTO {self.token_tablename} (expiration, jeton)"
            statement += " VALUES (?, ?);"
            cursor.execute(statement, (date_str,  db_token.jeton))
            rows = cursor.fetchall()


        return True
    
    def get_db_token(self, token : str) -> JetonValideDB:
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()
            
            statement  = "SELECT id, expiration, jeton"
            statement +=f" FROM {self.token_tablename}"
            statement +=f" WHERE jeton = '{token}'"
    
            cursor.execute(statement)
            result = cursor.fetchone()

            if result :
                db_token = self.load_token(result)
                return db_token
            
        return None
    
    def load_token(self, row) -> JetonValideDB :
        expiration_time = datetime.strptime(str(row[1]), self.date_format_string)
        db_token = JetonValideDB(
            id = int(row[0]),
            expiration=expiration_time,
            jeton = row[2]
        )
        return db_token
    
    def delete_token(self, db_token : JetonValideDB):
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

            statement  = f"DELETE FROM {self.token_tablename}"
            statement +=f" WHERE id = {db_token.id}"
            cursor.execute(statement)

        return True
    
    def delete_invalid_tokens(self) -> int :
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

            statement  = "SELECT id, expiration, jeton"
            statement +=f" FROM {self.token_tablename}"
 
            cursor.execute(statement)
            rows = cursor.fetchall()

            if len(rows) == 0:
                return None

            token_list = list()
            for row in rows:
                token_list.append(self.load_token(row))

            token_list : List[JetonValideDB] = token_list

            now = datetime.now(timezone.utc)

            for db_token in token_list :
                expiration = db_token.expiration.replace(tzinfo=timezone.utc)
                if now > expiration :
                    self.delete_token(db_token)

        return True 
    
    
    
