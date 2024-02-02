from app.dal.models.auth.user import User


class GetUserByIdTask:
    async def run(self, id: int) -> User | None:
        user = await User.filter(id=id).first()
        return user
