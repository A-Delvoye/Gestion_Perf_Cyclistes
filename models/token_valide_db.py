from pydantic import BaseModel
from datetime import datetime

class TokenValideDB():
    id: int 
    expires : datetime 
    token : str 