from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, joinedload

from app.core.models.roll_call.roll_call import RollCall
from app.core.models.roll_call.sick_leave import SickLeave
from app.routers.roll_call.view_models import RollCallViewModel, RollCallStatusEnum
from app.dal import get_session


class DeleteRollCallUseCase:
    def __init__(
            self,  session: Annotated[sessionmaker, Depends(get_session)],
    ):
        self.session = session

    def execute(self, roll_call_id: int) -> None:
        with self.session() as session:
            roll_call: RollCall = session.query(RollCall).options(
                joinedload(RollCall.sick_leave),
                joinedload(RollCall.location),
            ).get(roll_call_id)
            if not roll_call:
                raise HTTPException(status_code=404, detail="Roll call not found")
            if roll_call.sick_leave:
                session.delete(roll_call.sick_leave)
            if roll_call.location:
                session.delete(roll_call.location)
            session.delete(roll_call)
            session.commit()
