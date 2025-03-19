from fastapi import HTTPException, status
from datetime import datetime, timezone
from typing import Optional

# application imports
from db.db_session import DB_Session
from models.utilisateur_db import DB_User

def get_current_user(payload, need_activated_user:bool = True) -> DB_User :
    """
    raise HTTP_404_NOT_FOUND or HTTP_401_UNAUTHORIZED Exception
    """

    db_session = DB_Session()

    data_username = payload.get("sub")
    data_id = payload.get("id")

    # statement = select(UserInDb).where(UserInDb.id == data_id)
    # user = db_session.exec(statement).one_or_none()

    user = db_session.get_user_by_id(data_id)

    raise_user_exceptions(need_activated_user, user)
    
    return user

def get_current_admin(payload, need_activated_user:bool = True) -> DB_User :
    """
    raise HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED or HTTP_403_FORBIDDEN Exception
    """

    db_session = DB_Session()

    data_username = payload.get("sub")
    data_id = payload.get("id")

    # statement = select(UserInDb).where(UserInDb.id == data_id)
    # user = db_session.exec(statement).one_or_none()

    user = db_session.get_user_by_id(data_id)
    
    raise_user_exceptions(need_activated_user, user)

    if user.role != "admin" :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not enough permissions")
    
    return user

def raise_user_exceptions(need_activated_user: bool, user : Optional[DB_User]):
    if not user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found")
    
    if need_activated_user :
        if not user.is_active : 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="User not activated")

