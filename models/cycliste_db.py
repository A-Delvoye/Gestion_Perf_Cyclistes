from pydantic import BaseModel
from typing import Optional

class CyclisteDB():
    id_utilisateur : int
    nom : str
    age : int 
    poids : float
    taille : float
    sexe : int
