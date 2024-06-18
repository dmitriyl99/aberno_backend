from typing import Annotated

from fastapi import Depends

from app.core.services.auth import JWTAuthService
from app.tasks.auth.get_user_by_employee_number import GetUserByEmployeeNumberTask

from passlib.context import CryptContext


class CreateTokenUseCase:
    pwd_context: CryptContext

    def __init__(self, get_user_by_employee_number_task: Annotated[GetUserByEmployeeNumberTask, Depends(GetUserByEmployeeNumberTask)]):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
        self.get_user_by_employee_number_task = get_user_by_employee_number_task

    def execute(self, username: str, password: str) -> dict | None:
        user = self.get_user_by_employee_number_task.run(username)
        if user is None:
            return None
        password_verified = self.pwd_context.verify(password, user.password)
        if not password_verified:
            return None
        access_token = JWTAuthService.generate_token(subject={"sub": str(user.id)})

        return {
            'access_token': access_token,
            'type': 'bearer'
        }

