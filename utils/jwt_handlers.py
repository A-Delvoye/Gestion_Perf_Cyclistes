from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException, status
import jwt

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from schemas.auth_data import Token

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> tuple[str, datetime]:
    """
    Crée un token d'accès JWT.

    :param data: Données à inclure dans le token.
    :param expires_delta: Durée de validité du token (optionnelle).
    :return: Tuple contenant la date d'expiration et le token encodé.
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES//2)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return (expire, encoded_jwt)

def verify_token(token: str) :
    """
    Vérifie la validité d'un token JWT.

    :param token: Token JWT à vérifier.
    :raises HTTPException: Si le token est invalide ou expiré.
    raise HTTP_401_UNAUTHORIZED Exception

    :return: Le payload décodé du token.

    """
    
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except jwt.PyJWTError :
        raise credentials_exception
    
    if payload is None : 
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    return payload

