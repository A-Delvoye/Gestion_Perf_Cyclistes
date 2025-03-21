from datetime import datetime, timezone

#application imports
from db.db_session import DB_Session 
from models.jeton_valide_db import JetonValideDB

def register_token(token : str, expired_time: datetime): 
    db_token  = JetonValideDB(expiration = expired_time, jeton = token)
    db_session = DB_Session()
    db_session.insert_token(db_token)

def is_valid_token(token : str) -> bool :
    db_session = DB_Session()
    db_token = db_session.get_db_token(token)
    if not db_token :
        return False
    
    now = datetime.now(timezone.utc)
    expiration = db_token.expiration.replace(tzinfo=timezone.utc)

    if now > expiration :
        return False
    
    return True
    
def invalidate_token(token : str)  :
    db_session = DB_Session()
    db_token = db_session.get_db_token(token)
 
    if db_token :
        db_session.delete_token(db_token)

def clean_tokens() : 
    db_session = DB_Session()
    db_tokens = db_session.delete_invalid_tokens() 




    
