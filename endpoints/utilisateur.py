from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List


# application imports
from core.password_tools import verify_password, get_password_hash
from core.user_role_tools import get_current_user
from core.api_roles import ApiRole

from db.db_session import DB_Session
from db.token_white_list import register_token, is_valid_token, invalidate_token

from models.utilisateur_db import UtilisateurDB
from schemas.user_data import UserInfoData, UserCreateData, UserUpdateData
from schemas.auth_data import Token
from utils.jwt_handlers import verify_token

router = APIRouter()

utilisateur_scheme = OAuth2PasswordBearer(tokenUrl="/utilisateur")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)

#______________________________________________________________________________
#
# region Création d'un utilisateur (coach ou cycliste)
#______________________________________________________________________________
@router.post("/utilisateur", response_model=UserInfoData)
def create_utilisateur(
    creation_data: UserCreateData, 
    token : str = Depends(utilisateur_scheme)) -> UserInfoData:
    """
    Crée un nouvel utilisateur dans la base de données.

    Args:
        creation_data (UserCreateData): Les informations nécessaires pour créer un utilisateur 
            (nom d'utilisateur, email, mot de passe et rôle).
        token (str): Jeton d'authentification requis pour valider l'opération.

    Returns:
        UserInfoData: Les informations de l'utilisateur nouvellement créé (id, username, email, rôle).

    Raises:
        HTTPException 401: Si le token est invalide ou expiré.
        HTTPException 401: Si un utilisateur avec le même nom existe déjà.
        HTTPException 401: Si un utilisateur non-admin tente de créer un admin.
        HTTPException 403: Si le rôle fourni n'est pas valide.
        HTTPException 404: Si l'utilisateur n'a pas pu être récupéré après sa création.
    """

    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)

    db_session = DB_Session()
    creating_user = db_session.get_user_by_name(creation_data.username)
    if creating_user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A user with the same username allready exists")

    if creation_data.role == ApiRole.admin.value :
        if db_user.role != ApiRole.admin.value :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only an admin can create an admin")

    if creation_data.role not in [role.value for role in ApiRole] :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Impossible to create a user with role {creation_data.role} ")
        
    creating_user = UtilisateurDB(
        username = creation_data.username,
        email=creation_data.email,
        password_hash = get_password_hash(creation_data.password),
        role = creation_data.role)

    # insert in database
    db_session.create_user(creating_user)

    created_user = db_session.get_user_by_name(creating_user.username)
    if not created_user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Impossible to retrieve the created user")

    user_info_data = UserInfoData(
        id = created_user.id,
        username = created_user.username,
        email = created_user.email,
        role= created_user.role)     
         
    return user_info_data

#______________________________________________________________________________
#
# region Modification d'un utilisateur (coach ou cycliste)
#______________________________________________________________________________
@router.put("/utilisateur", response_model=UserInfoData)
def update_utilisateur(
    update_data: UserUpdateData, 
    token : str = Depends(utilisateur_scheme)) -> UserInfoData:
    """
    Met à jour les informations d'un utilisateur existant.

    Args:
        update_data (UserUpdateData): Données mises à jour de l'utilisateur, 
            incluant l'ID, le nom d'utilisateur, l'email, le nouveau mot de passe, 
            l'ancien mot de passe (si applicable) et le rôle.
        token (str): Jeton d'authentification requis pour valider l'opération.

    Returns:
        UserInfoData: Les informations mises à jour de l'utilisateur (id, username, email, rôle).

    Raises:
        HTTPException 401: Si le token est invalide ou expiré.
        HTTPException 401: Si l'ancien mot de passe ne correspond pas pour un utilisateur non-admin.
        HTTPException 401: Si un utilisateur non-admin tente d'attribuer le rôle admin.
        HTTPException 403: Si le rôle fourni n'est pas valide.
        HTTPException 404: Si l'utilisateur à mettre à jour n'est pas trouvé.
    """

    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)

    db_session = DB_Session()
    updating_user = db_session.get_user_by_id(update_data.id)
    if not updating_user :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Existing user not found")

    updating_user : UtilisateurDB = updating_user

    if db_user.role != ApiRole.admin.value:
        # the admin don't need to check old password to change values
        if not verify_password(update_data.old_password, updating_user.password_hash): 
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="The old password doesn't match")
    
    match update_data.role :
        case ApiRole.admin.value :
            if db_user.role != ApiRole.admin.value : 
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Only an admin can create an admin")
            
        case ApiRole.cycliste.value :
            pass

        case _ :
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Impossible to create a user with role {update_data.role} ")

    updating_user = UtilisateurDB(
        id=updating_user.id,
        username = update_data.username,
        email=update_data.email,
        password_hash = get_password_hash(update_data.new_password),
        role = update_data.role
    )

    db_session.update_user(updating_user)

    updated_user = db_session.get_user_by_id(updating_user.id)

    user_info_data = UserInfoData(
        id = updated_user.id,
        username = updated_user.username,
        email = updated_user.email, 
        role= updated_user.role)     
    return user_info_data

#______________________________________________________________________________
#
# region Suppression d'un utilisateur (coach ou cycliste)
#______________________________________________________________________________
@router.delete("/utilisateur/{id_utilisateur}")
def delete_utilisateur(
    id_utilisateur : int, 
    token : str = Depends(utilisateur_scheme)) -> UserInfoData:
    """
    Supprime un utilisateur de la base de données.

    Args:
        id_utilisateur (int): L'identifiant de l'utilisateur à supprimer.
        token (str): Jeton d'authentification requis pour valider l'opération.

    Returns:
        UserInfoData: Les informations de l'utilisateur effectuant la suppression (email, username, rôle).

    Raises:
        HTTPException 401: Si le token est invalide ou expiré.
        HTTPException 401: Si un utilisateur non-admin tente de supprimer un admin.
        HTTPException 401: Si l'utilisateur n'a pas été supprimé correctement.
        HTTPException 404: Si l'utilisateur à supprimer n'est pas trouvé.
    """

    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)

    db_session = DB_Session()
    deleting_user = db_session.get_user_by_id(id_utilisateur)

    if deleting_user.role == ApiRole.admin.value :
        if db_user.role != ApiRole.admin.value :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only an admin can delete an admin")
    
    db_session.delete_user(deleting_user.id)
 
    if db_session.get_user_by_id(deleting_user.id) :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"User {id_utilisateur} has not been deleted")

    user_info_data = UserInfoData(
        email = db_user.email, 
        username = db_user.username,
        role= db_user.role)     
         
    return user_info_data


#______________________________________________________________________________
#
# region Liste des utilisateurs 
#______________________________________________________________________________
@router.get("/utilisateur", response_model=List[UserInfoData])
def get_utilisateurs(
    token : str  = Depends(utilisateur_scheme), 
    ) -> list[UserInfoData]:
    """
    Récupère la liste de tous les utilisateurs.

    Args:
        token (str): Jeton d'authentification requis pour valider l'opération.

    Returns:
        list[UserInfoData]: Une liste contenant les informations de tous les utilisateurs 
            (nom d'utilisateur, email, rôle).

    Raises:
        HTTPException 401: Si le token est invalide ou expiré.
    """

    if not is_valid_token(token) :
        raise unauthorised_exception
    
    payload = verify_token(token)
    db_user = get_current_user(payload)

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




