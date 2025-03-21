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

