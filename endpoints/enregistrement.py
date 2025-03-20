from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List

# application imports
from core.password_tools import get_password_hash
from core.user_role_tools import get_current_user
from core.api_roles import ApiRole

from db.db_session import DB_Session
from db.db_session_record import DB_Session_Record
from db.token_white_list import is_valid_token

from models.utilisateur_db import UtilisateurDB
from models.enregistrement_db import EnregistrementDB
from schemas.record_data import RecordInfoData
from schemas.auth_data import Token
from utils.jwt_handlers import verify_token

router = APIRouter()


record_scheme = OAuth2PasswordBearer(tokenUrl="/enregistrement")

unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token d'authentification invalide",
    headers={"WWW-Authenticate": "Bearer"},
)

#______________________________________________________________________________
#
# region Création d'un Enregistrement 
#______________________________________________________________________________
@router.post("/enregistrement", response_model=RecordInfoData)
def create_record(
    record_data: RecordInfoData, 
    token : str = Depends(record_scheme)) -> RecordInfoData:

    if not is_valid_token(token) :
        raise unauthorised_exception

    payload = verify_token(token)
    db_user = get_current_user(payload)
    
    db_record = EnregistrementDB(
        id_utilisateur = record_data.id_utilisateur, 
        date = record_data.date,
        puissance_max= record_data.puissance_max,
        vo2_max = record_data.vo2_max,
        cadence_max = record_data.cadence_max,
        f_cardiaque_max = record_data.f_cardiaque_max,
        f_respiratoire_max = record_data.f_respiratoire_max)

    db_session = DB_Session_Record()
    db_session.insert_record(db_record)

    return record_data

#______________________________________________________________________________
#
# region Liste des enregistrements
#______________________________________________________________________________
@router.get("/enregistrement", response_model=List[RecordInfoData])
def get_enregistrement(
    user_id : int = 0,
    token : str  = Depends(record_scheme), 
    ) -> list[RecordInfoData]:

    if not is_valid_token(token) :
        raise unauthorised_exception
    
    payload = verify_token(token)
    db_user = get_current_user(payload)
    if user_id ==0 : 
        user_id = db_user.id


    db_session_record = DB_Session_Record()
    db_records : list[EnregistrementDB] = db_session_record.get_record_list(user_id)

    record_list = []
    for db_record in db_records :
        record_list.append(
            RecordInfoData (
                id=db_record.id,
                id_utilisateur = db_record.id_utilisateur, 
                date = db_record.date,
                puissance_max = db_record.puissance_max,
                vo2_max = db_record.vo2_max,
                cadence_max =  db_record.cadence_max,
                f_cardiaque_max = db_record.f_cardiaque_max, 
                f_respiratoire_max =  db_record.f_respiratoire_max))
        
    record_list : list[RecordInfoData] = record_list
    return record_list

