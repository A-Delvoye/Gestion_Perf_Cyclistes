from pydantic import BaseModel
from typing import Optional

#______________________________________________________________________________
#
# region User information data
#______________________________________________________________________________
class UserInfoData(BaseModel):
    """
    User information data 
    """
    username: str
    email : Optional [str] = None
    role: str = "cycliste"

#______________________________________________________________________________
#
# region Creation data needed for a User 
#______________________________________________________________________________
class UserCreationData(UserInfoData):
    """
    All data plus 'password' field
    """
    password : str



