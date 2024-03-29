from contextlib import asynccontextmanager

from fastapi import FastAPI
from tortoise import Tortoise

from app.routers.auth import authentication
from app.settings import TORTOISE_ORM


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(config=TORTOISE_ORM)

    yield

    await Tortoise.close_connections()


app = FastAPI(debug=True, title="Aberno API", lifespan=lifespan)

app.include_router(router=authentication.router, prefix='/api/auth')


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}
