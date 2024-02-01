from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    type: str


class LoginForm(BaseModel):
    phone: str
    password: str
