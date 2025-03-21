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
    id : Optional[int] = None
    username: str
    email : Optional [str] = None
    role: str = "cycliste"

#______________________________________________________________________________
#
# region Creation data needed for a User 
#______________________________________________________________________________
class UserCreateData(UserInfoData):
    """
    All data plus 'password' field
    """
    password : str


#______________________________________________________________________________
#
# region Creation data needed for a User 
#______________________________________________________________________________
class UserUpdateData(UserInfoData):
    """
    All data plus 'passwords' fields
    """
    old_password : str
    new_password : str


