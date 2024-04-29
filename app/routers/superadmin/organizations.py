from typing import Annotated, List

from fastapi import APIRouter, Depends, status, HTTPException

from app.use_cases.organization import (CreateOrganizationUseCase, GetOrganizationByIdUseCase,
                                        GetOrganizationsCase, UpdateOrganizationUseCase,
                                        DeleteOrganizationUseCase, UpdateOrganizationSettingsUseCase)
from .view_models import CreateOrganizationViewModel, OrganizationResponse, OrganizationSettingsViewModel
from app.core.facades.auth import Auth
from ...tasks.organization.get_current_employee_task import GetCurrentEmployeeTask

router = APIRouter(prefix='/organizations', tags=['admin-organizations'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[OrganizationResponse])
async def get_organizations(
        get_organizations_use_case: Annotated[GetOrganizationsCase, Depends(GetOrganizationsCase)],
        search: str | None = None,
):
    organizations = get_organizations_use_case.execute(search)

    return list(
        map(
            lambda organization: OrganizationResponse.from_model(organization), organizations
        )
    )


@router.get('/settings',
            status_code=status.HTTP_200_OK, response_model=OrganizationSettingsViewModel)
async def get_organization_settings(
        get_organization_by_id_use_case: Annotated[
            GetOrganizationByIdUseCase, Depends(GetOrganizationByIdUseCase)],
        get_current_employee_task: Annotated[
            GetCurrentEmployeeTask, Depends(GetCurrentEmployeeTask)
        ]
):
    employee = get_current_employee_task.run(Auth.get_current_user())
    organization = get_organization_by_id_use_case.execute(employee.organization_id)
    settings = organization.settings

    return OrganizationSettingsViewModel(
        roll_call_start_time=settings.roll_call_start_time if settings else None,
        roll_call_end_time=settings.roll_call_end_time if settings else None
    )


@router.put('/settings',
            status_code=status.HTTP_200_OK, response_model=OrganizationSettingsViewModel)
async def update_organization_settings(
        update_organization_use_case: Annotated[
            UpdateOrganizationSettingsUseCase, Depends(UpdateOrganizationSettingsUseCase)],
        data: OrganizationSettingsViewModel
):
    settings = update_organization_use_case.execute(Auth.get_current_user(), data)

    return OrganizationSettingsViewModel(
        roll_call_start_time=settings.roll_call_start_time,
        roll_call_end_time=settings.roll_call_end_time
    )


@router.get('/{organization_id}', response_model=OrganizationResponse)
async def get_organization(
        organization_id: int,
        get_organization_by_id_use_case: Annotated[GetOrganizationByIdUseCase, Depends(GetOrganizationByIdUseCase)]
):
    organization = get_organization_by_id_use_case.execute(organization_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Organization with id {} not found'.format(organization_id)
        )

    return OrganizationResponse.from_model(organization)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=OrganizationResponse)
async def create_organization(
        organization: CreateOrganizationViewModel,
        create_organization_use_case: Annotated[CreateOrganizationUseCase, Depends(CreateOrganizationUseCase)]
):
    organization = create_organization_use_case.execute(organization)

    return OrganizationResponse.from_model(organization)


@router.put('/{organization_id}', status_code=status.HTTP_200_OK, response_model=OrganizationResponse)
async def update_organization(
        organization: CreateOrganizationViewModel,
        organization_id: int,
        update_organization_use_case: Annotated[UpdateOrganizationUseCase, Depends(UpdateOrganizationUseCase)]
):
    organization = update_organization_use_case.execute(organization_id, organization)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Organization with id {} not found'.format(organization_id)
        )

    return OrganizationResponse.from_model(organization)


@router.delete('/{organization_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
        organization_id: int,
        delete_organization_use_case: Annotated[DeleteOrganizationUseCase, Depends(DeleteOrganizationUseCase)]
):
    result = delete_organization_use_case.execute(organization_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Organization with id {} not found'.format(organization_id)
        )
