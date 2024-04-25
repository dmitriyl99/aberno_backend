from fastapi import APIRouter, Depends

from app.dependencies import verify_authenticated_user, verify_admin_user

from app.routers.superadmin import organizations


router = APIRouter(
    prefix='/admin',
    tags=['admin'],
    dependencies=[Depends(verify_authenticated_user), Depends(verify_admin_user)]
)
router.include_router(organizations.router)
