from pydantic import BaseModel, Field
from typing import Optional
from constants.roles import Roles

class RegistrationUser(BaseModel):
    email: str = Field(pattern=r".+@.+")
    fullName: str
    password: str = Field(min_length=8)
    passwordRepeat: str
    roles: list[Roles]
    banned: Optional[bool] = None
    verified: Optional[bool] = None





