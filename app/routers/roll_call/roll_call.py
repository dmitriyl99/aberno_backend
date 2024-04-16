from . import router

from .view_models import RollCallViewModel

from app.core.facades.auth import Auth


@router.post("/")
async def create_roll_call(
        roll_call: RollCallViewModel
):
    user = Auth.get_current_user()
