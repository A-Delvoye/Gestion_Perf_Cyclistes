import sqlite3
from models.enregistrement_db import EnregistrementDB
from models.jeton_valide_db import JetonValideDB
from datetime import datetime, timezone
from core.config import DB_NAME

class DB_Session_Record() :
    def __init__(self) :
        self.database_path  = DB_NAME
        self.record_tablename = "enregistrements"
        self.date_format_string = "%Y-%m-%d %H:%M:%S.%f"


    def insert_record(self, db_record: EnregistrementDB) :
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

            date_str = db_record.date.strftime(self.date_format_string)

            statement = f"INSERT INTO {self.record_tablename} (id_utilisateur, date,"
            statement +=" puissance_max, vO2_max, cadence_max,"
            statement +=" f_cardiaque_max, f_respiratoire_max)"
            statement +=" VALUES (?, ?, ?, ?, ?, ?, ?);"
            
            # values = (db_record.id_utilisateur, 
            #           date_str, 
            #         f"{db_record.puissance_max:.2f}" , 
            #         f"{db_record.vo2_max:.2f}", 
            #         f"{db_record.cadence_max:.2f}",
            #         f"{db_record.f_cardiaque_max:.2f}", 
            #         f"{db_record.f_cardiaque_max:.2f}")

            values = (db_record.id_utilisateur, 
                      date_str, 
                      db_record.puissance_max , 
                      db_record.vo2_max, 
                      db_record.cadence_max,
                      db_record.f_cardiaque_max, 
                      db_record.f_cardiaque_max)

            cursor.execute(statement,values)
  
            connection.commit()

        return True
    
    def get_record_list(self, user_id : int) -> list[EnregistrementDB] :
        record_list = list()
        with sqlite3.connect(self.database_path) as connection : 
            cursor : sqlite3.Cursor = connection.cursor()

            statement = f"SELECT id, id_utilisateur, date, puissance_max, vO2_max, cadence_max, f_cardiaque_max, f_respiratoire_max"
            statement +=f" FROM {self.record_tablename}"
            statement +=f" WHERE id_utilisateur = {user_id}"

            cursor.execute(statement)
            rows = cursor.fetchall()
            for row in rows:
                record_list.append(self.load_record(row))

        record_list : list[EnregistrementDB] = record_list

        return record_list   

    
    def load_record(self, row) -> EnregistrementDB :

        record_date =  datetime.strptime(str(row[2]), self.date_format_string)

        db_record = EnregistrementDB(
            id = int(row[0]), 
            id_utilisateur = int(row[1]), 
            date = record_date, 
            puissance_max = float(row[3]), 
            vo2_max = float(row[4]), 
            cadence_max = float(row[5]), 
            f_cardiaque_max = float(row[6]), 
            f_respiratoire_max = float(row[7]), 
        )
        return db_record