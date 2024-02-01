from typing import Annotated

from fastapi import Depends
from app.dal.models.auth.user import User
from app.tasks.auth.create_jwt_token_task import CreateJWTTokenTask
from passlib.context import CryptContext


class CreateTokenUseCase:
    pwd_context: CryptContext
    create_jwt_token_task: CreateJWTTokenTask

    def __init__(self, create_jwt_token_task: Annotated[CreateJWTTokenTask, Depends(CreateJWTTokenTask)]):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
        self.create_jwt_token_task = create_jwt_token_task

    async def execute(self, phone: str, password: str) -> dict | None:
        user = await User.filter(phone=phone).first()
        if user is None:
            return None
        password_verified = self.pwd_context.verify(password, user.password)
        if not password_verified:
            return None
        access_token = self.create_jwt_token_task.run(data={"sub": user.phone})

        return {
            'access_token': access_token,
            'type': 'bearer'
        }

