from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class JetonValideDB(BaseModel):
    id: Optional[int] = None
    expiration : datetime 
    jeton : str 