from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.core.models.auth import User


class Token(BaseModel):
    access_token: str
    type: str


class LoginForm(BaseModel):
    username: str
    password: str


class FirebaseToken(BaseModel):
    token: str


class RoleViewModel(BaseModel):
    id: int
    name: str


class PermissionViewModel(BaseModel):
    id: int
    name: str


class CurrentUserViewModel(BaseModel):
    id: int
    name: str
    last_name: str | None
    username: str | None
    employee_number: str | None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    roles: List[RoleViewModel] | None = None
    permissions: List[PermissionViewModel] | None = None

    @staticmethod
    def from_model(user: User):
        response = CurrentUserViewModel(
            id=user.id,
            name=user.name,
            last_name=user.last_name,
            is_active=user.is_active,
            username=user.username,
            employee_number=user.employee_number,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        if 'roles' in user.__dict__:
            response.roles = list(map(lambda x: RoleViewModel(
                id=x.id,
                name=x.name
            ), user.roles))
        if 'permissions' in user.__dict__:
            response.permissions = list(map(lambda x: PermissionViewModel(
                id=x.id,
                name=x.name
            ), user.permissions))

        return response
