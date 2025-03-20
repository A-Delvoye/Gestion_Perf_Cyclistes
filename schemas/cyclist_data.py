from pydantic import BaseModel
from typing import Optional

#______________________________________________________________________________
#
# region Information sur un Cycliste 
#______________________________________________________________________________
class CyclistInfoData(BaseModel):
    """
    Cyclist information data 
    """
    id_utilisateur : int
    nom_cycliste : str
    age : int
    poids : float
    taille : float
    sexe : bool