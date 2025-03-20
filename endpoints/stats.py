from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from utils.db_utils import get_db_connection

router = APIRouter()


#______________________________________________________________________________
#
# region Puissance_max all 
#______________________________________________________________________________

@router.get("/stats/puissance_max_globale")
def get_max_puissance_globale():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Récupérer la puissance max la plus élevée de tous les coureurs
    cursor.execute("SELECT MAX(puissance_max) FROM enregistrements")
    max_puissance = cursor.fetchone()[0]
    
    conn.close()

    if max_puissance is None:
        raise HTTPException(status_code=404, detail="Aucune donnée de puissance trouvée")

    return {"puissance_max_globale": max_puissance}

#______________________________________________________________________________
#
# region Puissance_max of a given cyclist  
#______________________________________________________________________________

@router.get("/stats/puissance_max_cycliste/{coureur_id}")
def get_max_puissance_coureur(coureur_id: int):
    conn = get_db_connection()
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

    conn.close()

    if max_puissance is None:
        raise HTTPException(status_code=404, detail="Aucune donnée de puissance trouvée pour ce coureur")

    return {"coureur_id": coureur_id, "puissance_max": max_puissance}
