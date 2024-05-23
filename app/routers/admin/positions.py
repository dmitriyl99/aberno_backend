from typing import Annotated, List

from fastapi import APIRouter, Depends
from starlette import status

from app.use_cases.organization.positions import (
    CreatePositionUseCase,
    DeletePositionUseCase,
    UpdatePositionUseCase,
    GetPositionsUseCase
)
from .view_models import PositionViewModel, CreatePositionViewModel


router = APIRouter(prefix='/positions', tags=['positions'])


@router.get('/', response_model=List[PositionViewModel])
def get_positions(
        get_positions_use_case: Annotated[GetPositionsUseCase, Depends(GetPositionsUseCase)],
        organization_id: int | None = None
):
    return list(
        map(lambda position: PositionViewModel.from_model(position), get_positions_use_case.execute(organization_id))
    )


@router.post('/', response_model=PositionViewModel)
def create_position(
        create_position_use_case: Annotated[CreatePositionUseCase, Depends(CreatePositionUseCase)],
        data: CreatePositionViewModel
):
    position = create_position_use_case.execute(data.name, data.organization_id)
    return PositionViewModel.from_model(position)


@router.put('/{id}', response_model=PositionViewModel)
def update_position(
        update_position_use_case: Annotated[UpdatePositionUseCase, Depends(UpdatePositionUseCase)],
        id: int,
        data: CreatePositionViewModel,
):
    position = update_position_use_case.execute(id, data.name)
    return PositionViewModel.from_model(position)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_position(
        delete_position_use_case: Annotated[DeletePositionUseCase, Depends(DeletePositionUseCase)],
        id: int
):
    delete_position_use_case.execute(id)
