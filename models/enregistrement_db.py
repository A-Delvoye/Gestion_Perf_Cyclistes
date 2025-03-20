from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EnregistrementDB(BaseModel) :
    id: Optional[int] = None
    id_utilisateur : int
    date : datetime
    puissance_max : float
    vo2_max : float
    cadence_max : float
    f_cardiaque_max : float
    f_respiratoire_max : float