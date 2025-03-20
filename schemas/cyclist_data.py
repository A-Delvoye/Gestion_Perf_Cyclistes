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
    nom : str
    age : int
    poids : float
    taille : float
    sexe : str
    utilisateur_id : int

class CyclisteUpdate(BaseModel):
    nom: str
    age: int
    poids: float
    taille: float
    sexe: str

class CyclisteCreate(BaseModel):
    nom: str
    age: int
    poids: float
    taille: float
    sexe: str