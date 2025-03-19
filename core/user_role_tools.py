from fastapi import HTTPException, status
from datetime import datetime, timezone
from typing import Optional

# application imports
from db.db_session import DB_Session
from models.utilisateur_db import UtilisateurDB

def get_current_user(payload) -> UtilisateurDB :
    """
    raise HTTP_404_NOT_FOUND
    """

    db_session = DB_Session()

    data_username = payload.get("sub")
    data_id = payload.get("id")

    user = db_session.get_user_by_id(data_id)

    raise_user_exceptions(user)
    
    return user

def get_current_admin(payload) -> UtilisateurDB :
    """
    raise HTTP_404_NOT_FOUND or HTTP_401_UNAUTHORIZED
    """

    db_session = DB_Session()

    data_username = payload.get("sub")
    data_id = payload.get("id")

    user = db_session.get_user_by_id(data_id)
    
    raise_user_exceptions(user)

    if user.role != "admin" :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Not enough permissions")
    
    return user

def raise_user_exceptions(user : Optional[UtilisateurDB]):
    if not user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found")
    

