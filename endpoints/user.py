from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List


# application imports
from core.password_tools import get_password_hash
from core.user_role_tools import get_current_user
from core.api_roles import ApiRole

from db.db_session import DB_Session
from db.token_white_list import register_token, is_valid_token, invalidate_token

from models.utilisateur_db import UtilisateurDB
from schemas.user_data import UserInfoData, UserCreationData
from schemas.auth_data import Token
from utils.jwt_handlers import verify_token

router = APIRouter()

create_user_scheme = OAuth2PasswordBearer(tokenUrl="/user")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)

#______________________________________________________________________________
#
# region Création d'un user (coach ou cycliste)
#______________________________________________________________________________
@router.post("/user", response_model=UserInfoData)
def create_user(
    creation_data: UserCreationData, 
    token : str = Depends(create_user_scheme)) -> UserInfoData:

    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)

    if creation_data.role == ApiRole.admin.value :
        if db_user.role != ApiRole.admin.value :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only an admin can create an admin")

    if creation_data.role not in [role.value for role in ApiRole] :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Impossible to create a user with role {creation_data.role} ")
        
    db_user = UtilisateurDB(
        username = creation_data.username,
        email=creation_data.email,
        password_hash = get_password_hash(creation_data.password),
        role = creation_data.role)

    db_session = DB_Session()
    db_session.insert_user(db_user)

    user_info_data = UserInfoData(
        email = db_user.email, 
        username = db_user.username,
        role= db_user.role)     
         
    return user_info_data