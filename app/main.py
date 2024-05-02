from fastapi import FastAPI

from contextlib import asynccontextmanager

from app.routers.auth import authentication
from app.routers import organization, roll_call, admin
from app import schedule

from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    schedule.start()

    yield

    schedule.stop()


app = FastAPI(debug=settings.environment in ['local', 'debug'], title="Aberno API", lifespan=lifespan)

app.include_router(router=authentication.router, prefix='/api/auth')
for router in organization.routers:
    app.include_router(router, prefix='/api/organization', tags=['organizations'])
for router in roll_call.routers:
    app.include_router(router=router, prefix='/api')
app.include_router(admin.router, prefix='/api')
