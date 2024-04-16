from fastapi import APIRouter, Depends

from app.dependencies import verify_authenticated_user


router = APIRouter(dependencies=[Depends(verify_authenticated_user)])
