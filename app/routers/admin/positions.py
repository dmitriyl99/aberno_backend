from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from starlette import status

from app.use_cases.organization.positions import (
    CreatePositionUseCase,
    DeletePositionUseCase,
    UpdatePositionUseCase,
    GetPositionsUseCase
)
from .view_models import PositionViewModel, CreatePositionViewModel
from ...use_cases.organization.positions.get_position_by_id_use_case import GetPositionByIdUseCase

router = APIRouter(prefix='/positions', tags=['positions'])


@router.get('/', response_model=List[PositionViewModel])
def get_positions(
        get_positions_use_case: Annotated[GetPositionsUseCase, Depends(GetPositionsUseCase)],
        organization_id: int | None = None,
        department_id: int | None = None
):
    positions = get_positions_use_case.execute(organization_id, department_id)
    return list(
        map(lambda position: PositionViewModel.from_model(position), positions)
    )


@router.get('/{position_id}', response_model=PositionViewModel)
def get_positions(
        get_position_by_id_use_case: Annotated[GetPositionByIdUseCase, Depends(GetPositionByIdUseCase)],
        position_id: int | None = None,
):
    position = get_position_by_id_use_case.execute(position_id)
    if not position:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Position not found'
        )
    return PositionViewModel.from_model(position)


@router.post('/', response_model=PositionViewModel)
def create_position(
        create_position_use_case: Annotated[CreatePositionUseCase, Depends(CreatePositionUseCase)],
        data: CreatePositionViewModel
):
    position = create_position_use_case.execute(data.name, data.organization_id, data.department_id)
    return PositionViewModel.from_model(position)


@router.put('/{id}', response_model=PositionViewModel)
def update_position(
        update_position_use_case: Annotated[UpdatePositionUseCase, Depends(UpdatePositionUseCase)],
        id: int,
        data: CreatePositionViewModel,
):
    position = update_position_use_case.execute(id, data.name, data.department_id)
    return PositionViewModel.from_model(position)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_position(
        delete_position_use_case: Annotated[DeletePositionUseCase, Depends(DeletePositionUseCase)],
        id: int
):
    delete_position_use_case.execute(id)
