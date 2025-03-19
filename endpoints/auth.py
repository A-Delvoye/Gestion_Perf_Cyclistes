from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import timedelta

# application imports
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from core.password_tools import verify_password, get_password_hash
from core.user_role_tools import get_current_user
from db.token_white_list import register_token, is_valid_token, invalidate_token
from db.db_session import DB_Session

from schemas.auth_data import Token, AuthData
from utils.jwt_handlers import create_access_token, verify_token

from models.utilisateur_db import UtilisateurDB

router = APIRouter()

#login_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
logout_scheme = OAuth2PasswordBearer(tokenUrl="/auth/logout")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)

#______________________________________________________________________________
#
# region Connexion et récupération du token
#______________________________________________________________________________
@router.post("/auth/login", response_model=Token)
def login_for_access_token( auth_data: AuthData ) -> Token:
    """
    Connexion à l'API 'Gestion Performance Cyclistes' et récupération du jeton d'authentification
    """
    login_unauthorised_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Cherche l'utilisateur dans la base de données par son email
    # statement = select(UserInDb).where(UserInDb.email == auth_data.email)
    # db_user = db_session.exec(statement).one_or_none()
    db_session = DB_Session()
    db_user : UtilisateurDB = db_session.get_user_by_name(auth_data.username)

    # Vérifie si l'utilisateur existe et si le mot de passe est valide
    if not db_user :
        raise login_unauthorised_exception
    
    if not verify_password(auth_data.password, db_user.password_hash): 
        print(f"auth : {auth_data.password}, db : {db_user.password_hash}, test_hash ; {get_password_hash(auth_data.password)}")
        raise login_unauthorised_exception
         
    # Si l'utilisateur existe et que le mot de passe est valide, créer un token d'accès
    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    (expired_time, access_token) = create_access_token(
        data={"sub": db_user.username, "id" : db_user.id}, 
        expires_delta=access_token_expires
    )

    register_token(access_token, expired_time)

    # Retourne le token d'accès et le type de token
    return Token (access_token = access_token, token_type = "bearer")

#______________________________________________________________________________
#
# region Déconnexion
#______________________________________________________________________________
@router.post("/auth/logout")
def logout(token: str = Depends(logout_scheme)):
    """
    Déconnexion de l'API 'Gestion Performance Cyclistes'
    """

    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload, need_activated_user=False)
    
    invalidate_token(token)

    return {"msg": "Logged out successfully. Token is invalidated."}