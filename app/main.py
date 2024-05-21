from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from app.routers.auth import authentication
from app.routers import organization, roll_call, admin
from app.routers.tasks import tasks
from app import schedule
from firebase_admin import credentials, initialize_app
import os

from app.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    schedule.start()
    firebase_cred = credentials.Certificate(os.path.join(os.getcwd(), 'firebase-certificate.json'))
    initialize_app(firebase_cred)

    yield

    schedule.stop()


app = FastAPI(debug=settings.environment in ['local', 'debug'], title="Aberno API", lifespan=lifespan)

origins = [
    "http://localhost:5173"
]

app.add_middleware(CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
))

app.include_router(router=authentication.router, prefix='/api/auth')
for router in organization.routers:
    app.include_router(router, prefix='/api/organization', tags=['organizations'])
for router in roll_call.routers:
    app.include_router(router=router, prefix='/api')
app.include_router(admin.router, prefix='/api')
app.include_router(tasks.router, prefix='/api')
