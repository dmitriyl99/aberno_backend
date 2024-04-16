from fastapi import APIRouter, Depends

from .view_models import RollCallViewModel

from app.core.facades.auth import Auth
from app.dependencies import verify_authenticated_user


router = APIRouter(prefix='/roll-call', tags=['roll-call'], dependencies=[Depends(verify_authenticated_user)])


@router.post("/")
async def create_roll_call(
        roll_call: RollCallViewModel
):
    user = Auth.get_current_user()
