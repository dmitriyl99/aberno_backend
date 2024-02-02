from pydantic import BaseModel
from datetime import datetime


class Token(BaseModel):
    access_token: str
    type: str


class LoginForm(BaseModel):
    phone: str
    password: str


class CurrentUserViewModel(BaseModel):
    id: int
    name: str
    phone: str
    created_at: datetime
    updated_at: datetime
    roles: list
    permissions: list | None


class RoleViewModel(BaseModel):
    id: int
    name: str


class PermissionViewModel(BaseModel):
    id: int
    name: str

