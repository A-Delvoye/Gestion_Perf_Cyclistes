from pydantic import BaseModel
from typing import Optional

class DB_User(BaseModel):
    id: Optional[int] = None
    username : str 
    email: str 
    password_hash: str 
    role: str 
    