from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List


# application imports
from core.password_tools import get_password_hash
from core.user_role_tools import get_current_admin

from db.db_session import DB_Session
from db.token_white_list import register_token, is_valid_token, invalidate_token

from models.utilisateur_db import UtilisateurDB
from schemas.user_data import UserInfoData, UserCreationData
from schemas.auth_data import Token
from utils.jwt_handlers import verify_token

router = APIRouter()

cyclist_list_scheme = OAuth2PasswordBearer(tokenUrl="/coach/users")
stats_scheme = OAuth2PasswordBearer(tokenUrl="/coach/stats")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)

#______________________________________________________________________________
#
# region Liste des utilisateurs (Admin)
#______________________________________________________________________________
@router.get("/coach/users", response_model=List[UserInfoData])
def get_users(
    token : str  = Depends(cyclist_list_scheme), 
    ) -> list[UserInfoData]:
    """
    Récupère la liste des utilisateurs pour un coach.

    :param token: Jeton d'authentification OAuth2 récupéré via Depends.
    :raises HTTPException: Si le token est invalide.
    :return: Liste des utilisateurs sous forme d'objets UserInfoData.
    """

    if not is_valid_token(token) :
        raise unauthorised_exception
    
    payload = verify_token(token)
    db_admin = get_current_admin(payload)

    db_session = DB_Session()
    db_users = db_session.get_user_list()

    users_data = []
    for db_user in db_users :
        users_data.append(
            UserInfoData (
                username = db_user.username, 
                email = db_user.email,
                role = db_user.role))
        
    users_data : list[UserInfoData] = users_data
    return users_data




