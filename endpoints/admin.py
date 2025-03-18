from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List


# application imports
from core.password_tools import get_password_hash
from core.user_role_tools import get_current_admin

from db.db_session import DB_Session
from db.token_white_list import register_token, is_valid_token, invalidate_token

from models.user import DB_User
from schemas.user_data import UserInfoData, UserCreationData
from schemas.auth_data import Token
from utils.jwt_handlers import verify_token

router = APIRouter()

admin_scheme = OAuth2PasswordBearer(tokenUrl="/admin/users")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)

#______________________________________________________________________________
#
# region Liste des utilisateurs (Admin)
#______________________________________________________________________________
@router.get("/admin/users", response_model=List[UserInfoData])
def get_users(
    token : str  = Depends(admin_scheme), 
    ) -> list[UserInfoData]:

    if not is_valid_token(token, db_session) :
        raise unauthorised_exception
    
    payload = verify_token(token)
    db_admin = get_current_admin(payload, db_session)

    # statement = select(UserInDb)
    # db_users = db_session.exec(statement).all()

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

#______________________________________________________________________________
#
# region Création d'un utilisateur (Admin)
#______________________________________________________________________________
@router.post("/admin/users", response_model=UserInfoData)
def create_user(
    creation_data: UserCreationData, 
    token : str = Depends(admin_scheme)) -> UserInfoData:

    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_admin = get_current_admin(payload)

    if creation_data.role not in ["admin", "user"] :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Role does not exist")
    
    db_user = DB_User(
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
