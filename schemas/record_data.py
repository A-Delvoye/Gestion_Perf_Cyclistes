from pydantic import BaseModel
from typing import Optional
from datetime import datetime

#______________________________________________________________________________
#
# region Information sur un Enregistrement 
#______________________________________________________________________________
class RecordInfoData(BaseModel):
    """
    Record information data 
    """
    id: Optional[int] = None
    id_utilisateur : int
    date : datetime
    puissance_max : float
    vo2_max : float
    cadence_max : float
    f_cardiaque_max : float
    f_respiratoire_max :  float