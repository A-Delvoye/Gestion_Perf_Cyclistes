
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
from schemas.cyclist_data import CyclistInfoData, CyclisteUpdate, CyclisteCreate
from schemas.auth_data import Token
from utils.jwt_handlers import verify_token
from utils.db_utils import get_db_connection

router = APIRouter()

cycliste_scheme = OAuth2PasswordBearer(tokenUrl="/cycliste")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)


#______________________________________________________________________________
#
# region Affichage d'un Cycliste 
#______________________________________________________________________________

@router.get("/cycliste")
def get_cyclist_by_id(cycliste_id: int, 
    token : str = Depends(cycliste_scheme)) :

    """
    Récupère les informations d'un cycliste à partir de son ID.
    
    :param cycliste_id: Identifiant unique du cycliste.
    :return: Dictionnaire contenant les informations du cycliste.
    """
    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        requete = "SELECT * FROM cyclistes WHERE id = ?"
        cursor.execute(requete, (cycliste_id, ))
        results = dict(cursor.fetchone())
            
        return results
    return None
#______________________________________________________________________________
#
# region Update d'un Cycliste 
#______________________________________________________________________________
@router.put("/cycliste/{cycliste_id}")
def update_cycliste(cycliste_id: int, cycliste_data: CyclisteUpdate, 
    token : str = Depends(cycliste_scheme)) :
    """
    Met à jour les informations d'un cycliste existant.
    
    :param cycliste_id: Identifiant unique du cycliste.
    :param cycliste_data: Données mises à jour du cycliste.
    :return: Message confirmant la mise à jour du cycliste.
    """

    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Vérifier si le cycliste existe
        cursor.execute("SELECT * FROM cyclistes WHERE id = ?", (cycliste_id,))
        existing_cycliste = cursor.fetchone()
        
        if not existing_cycliste:
            conn.close()
            raise HTTPException(status_code=404, detail="Cycliste non trouvé")

        # Mise à jour des informations du cycliste
        requete = """
            UPDATE cyclistes
            SET nom = ?, age = ?, poids = ?, taille = ?, sexe = ?
            WHERE id = ?
        """
        cursor.execute(requete, (cycliste_data.nom, cycliste_data.age, cycliste_data.poids, 
                                cycliste_data.taille, cycliste_data.sexe, cycliste_id))
        conn.commit()
        
        return {"message": f"Cycliste ID {cycliste_id} mis à jour avec succès"}
    return None
#______________________________________________________________________________
#
# region Création d'un Cycliste 
#______________________________________________________________________________
@router.post("/cycliste")
def create_cycliste(cycliste_data: CyclisteCreate, 
    token : str = Depends(cycliste_scheme)) :
    """
    Crée un nouveau cycliste dans la base de données.
    
    :param cycliste_data: Données du cycliste à ajouter.
    :return: Message de confirmation et ID du cycliste créé.
    """
    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)

    with get_db_connection() as conn:
        cursor = conn.cursor()
    # Insérer le cycliste dans la base de données
        requete = """
            INSERT INTO cyclistes (nom, age, poids, taille, sexe)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(requete, (cycliste_data.nom, cycliste_data.age, cycliste_data.poids, 
                                cycliste_data.taille, cycliste_data.sexe))
        conn.commit()
        
        # Récupérer l'ID du cycliste inséré
        cycliste_id = cursor.lastrowid
        
        return {"message": "Cycliste créé avec succès", "id": cycliste_id}
    return None
#______________________________________________________________________________
#
# region Delete d'un Cycliste 
#______________________________________________________________________________

@router.delete("/cycliste/{cycliste_id}")
def delete_cycliste(cycliste_id: int, 
    token : str = Depends(cycliste_scheme)) :
    """
    Supprime un cycliste de la base de données.
    
    :param cycliste_id: Identifiant unique du cycliste à supprimer.
    :return: Message confirmant la suppression du cycliste.
    """
    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Vérifier si le cycliste existe
        cursor.execute("SELECT * FROM cyclistes WHERE id = ?", (cycliste_id,))
        existing_cycliste = cursor.fetchone()
        
        if not existing_cycliste:
            conn.close()
            raise HTTPException(status_code=404, detail="Cycliste non trouvé")

        # Supprimer le cycliste
        requete = "DELETE FROM cyclistes WHERE id = ?"
        cursor.execute(requete, (cycliste_id,))
        conn.commit()
        
        return {"message": f"Cycliste ID {cycliste_id} supprimé avec succès"}
    return None
