from fastapi import APIRouter, Depends

from app.dependencies import verify_authenticated_user, verify_admin_user

from app.routers.admin import organizations, departments, employees, roll_call


router = APIRouter(
    prefix='/admin',
    dependencies=[Depends(verify_authenticated_user), Depends(verify_admin_user)]
)
router.include_router(organizations.router)
router.include_router(departments.router)
router.include_router(employees.router)
router.include_router(roll_call.router)
