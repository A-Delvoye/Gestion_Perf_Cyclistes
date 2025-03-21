from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from utils.db_utils import get_db_connection
from core.user_role_tools import get_current_user
from utils.jwt_handlers import verify_token
from db.token_white_list import is_valid_token


router = APIRouter()

stats_scheme1 = OAuth2PasswordBearer(tokenUrl="/stats/puissance_max_globale")
stats_scheme2 = OAuth2PasswordBearer(tokenUrl="/stats/puissance_max_cycliste")


unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)

#______________________________________________________________________________
#
# region Puissance_max all 
#______________________________________________________________________________

@router.get("/stats/puissance_max_globale")
def get_max_puissance_globale(token : str = Depends(stats_scheme1)) :
    """
    Récupère la puissance maximale la plus élevée enregistrée parmi tous les coureurs.

    Args:
        token (str): Jeton d'authentification requis pour valider l'accès aux statistiques.

    Returns:
        dict: Un dictionnaire contenant la puissance maximale globale enregistrée :
            - "puissance_max_globale" (float): La valeur la plus élevée de puissance max.

    Raises:
        HTTPException 401: Si le token est invalide ou expiré.
        HTTPException 404: Si aucune donnée de puissance n'est trouvée dans la base.
    """

    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)


    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Récupérer la puissance max la plus élevée de tous les coureurs
        cursor.execute("SELECT MAX(puissance_max) FROM enregistrements")
        max_puissance = cursor.fetchone()[0]
        


        if max_puissance is None:
            raise HTTPException(status_code=404, detail="Aucune donnée de puissance trouvée")

        return {"puissance_max_globale": max_puissance}

#______________________________________________________________________________
#
# region Puissance_max of a given cyclist  
#______________________________________________________________________________

@router.get("/stats/puissance_max_cycliste/{coureur_id}")
def get_max_puissance_coureur(coureur_id, 
    token : str = Depends(stats_scheme2)) :
    """
    Récupère la puissance maximale enregistrée pour un coureur donné.

    Args:
        coureur_id (int): Identifiant unique du coureur dont on veut récupérer la puissance max.
        token (str): Jeton d'authentification requis pour valider l'accès aux statistiques.

    Returns:
        dict: Un dictionnaire contenant :
            - "coureur_id" (int): L'identifiant du coureur.
            - "puissance_max" (float): La valeur maximale de puissance enregistrée pour ce coureur.

    Raises:
        HTTPException 401: Si le token est invalide ou expiré.
        HTTPException 404: Si le coureur n'existe pas ou s'il n'a pas de données de puissance enregistrées.
    """


    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)


    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Vérifier si le coureur existe
        cursor.execute("SELECT id FROM cyclistes WHERE id = ?", (coureur_id,))
        existing_coureur = cursor.fetchone()

        if not existing_coureur:
            conn.close()
            raise HTTPException(status_code=404, detail="Coureur non trouvé")
        
        # Récupérer la puissance max du coureur
        cursor.execute("SELECT MAX(puissance_max) FROM enregistrements WHERE id = ?", (coureur_id,))
        max_puissance = cursor.fetchone()[0]


        if max_puissance is None:
            raise HTTPException(status_code=404, detail="Aucune donnée de puissance trouvée pour ce coureur")

        return {"coureur_id": coureur_id, "puissance_max": max_puissance}
