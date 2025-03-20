from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EnregistrementDB() :
    id: Optional[int] = None
    id_utilisateur : int
    puissance_max : float
    vo2_max : float
    cadence_max : float
    f_cardiaque_max : float
    f_respiratoire_max :  float