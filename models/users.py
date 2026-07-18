from pydantic import BaseModel

class RegistrationUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: list[str]





