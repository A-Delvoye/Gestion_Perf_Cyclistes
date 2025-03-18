from pydantic import BaseModel, Field
from typing import Optional

class DB_User(BaseModel):
    id: Optional[int] = Field(exclude=True)
    username : str = Field()
    email: str = Field()
    password_hash: str = Field()
    role: str = Field()