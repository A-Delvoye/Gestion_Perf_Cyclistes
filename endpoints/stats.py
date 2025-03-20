from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List
from utils.db_utils import get_db_connection


#______________________________________________________________________________
#
# region Puissance_max all 
#______________________________________________________________________________

router = APIRouter()

@router.get("/stats/puissance_max_globale")
def get_max_puissance_globale():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Récupérer la puissance max la plus élevée de tous les coureurs
    cursor.execute("SELECT MAX(puissance_max) FROM enregistrement")
    max_puissance = cursor.fetchone()[0]
    
    conn.close()

    if max_puissance is None:
        raise HTTPException(status_code=404, detail="Aucune donnée de puissance trouvée")

    return {"puissance_max_globale": max_puissance}