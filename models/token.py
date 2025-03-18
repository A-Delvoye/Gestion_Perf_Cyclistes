from pydantic import BaseModel
from datetime import datetime

class DB_Token():
    id: int 
    expires : datetime 
    token : str 