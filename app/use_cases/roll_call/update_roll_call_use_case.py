from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import sessionmaker, joinedload

from app.core.models.roll_call.roll_call import RollCall, RollCallStatusEnum
from app.core.models.roll_call.sick_leave import SickLeave
from app.routers.roll_call.view_models import RollCallViewModel
from app.dal import get_session


class UpdateRollCallUseCase:
    def __init__(
            self,  session: Annotated[sessionmaker, Depends(get_session)],
    ):
        self.session = session

    def execute(self, roll_call_id: int, dto: RollCallViewModel) -> RollCall:
        with self.session() as session:
            roll_call: RollCall = session.query(RollCall).options(joinedload(RollCall.sick_leave)).get(roll_call_id)
            roll_call.status = dto.status
            roll_call.note = dto.note
            if dto.status == RollCallStatusEnum.SICK and dto.sick_leave is not None:
                sick_leave = SickLeave(
                    note=dto.note,
                    date_from=dto.sick_leave.date_from,
                    date_to=dto.sick_leave.date_to,
                    employee_id=roll_call.employee_id
                )
                if roll_call.sick_leave:
                    session.delete(roll_call.sick_leave)
                roll_call.sick_leave = sick_leave
            session.commit()
            session.refresh(roll_call)

            return roll_call
