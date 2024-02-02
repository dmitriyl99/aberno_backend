from app.core.models.auth.user import User


class GetUserByPhoneTask:
    async def run(self, phone: str):
        user = await User.filter(phone=phone).first()
        return user
