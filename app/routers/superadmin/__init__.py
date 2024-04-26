from fastapi import APIRouter, Depends

from app.dependencies import verify_authenticated_user, verify_admin_user

from app.routers.superadmin import organizations, departments, employees


router = APIRouter(
    prefix='/admin',
    dependencies=[Depends(verify_authenticated_user), Depends(verify_admin_user)]
)
router.include_router(organizations.router)
router.include_router(departments.router)
router.include_router(employees.router)
