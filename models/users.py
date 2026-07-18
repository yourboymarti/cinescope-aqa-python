from pydantic import BaseModel
from typing import Optional
from constants.roles import Roles

class RegistrationUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[Roles]
    banned: Optional[bool] = None
    verified: Optional[bool] = None





