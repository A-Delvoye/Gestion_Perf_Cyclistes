from fastapi import APIRouter

from schemas.auth_data import Token, AuthData

router = APIRouter()

#______________________________________________________________________________
#
# region Connexion et récupération du token
#______________________________________________________________________________
@router.post("/auth/login", response_model=Token)
def login_for_access_token(auth_data: AuthData) -> Token:

    # Retourne le token d'accès et le type de token
    return Token (access_token = "Azerty123", token_type = "bearer")



#______________________________________________________________________________
#
# region Déconnexion
#______________________________________________________________________________
@router.post("/auth/logout")
def logout(token: str ):

    return {"msg": "Logged out successfully. Token is invalidated."}
