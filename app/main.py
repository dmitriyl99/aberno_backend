from fastapi import FastAPI
from tortoise import Tortoise

from app.routers.auth import authentication

app = FastAPI(debug=True, title="Aberno API")

app.include_router(router=authentication.router, prefix='/api/auth')


@app.on_event('startup')
async def on_startup():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': [
            'app.core.models.auth.user',
            'app.core.models.auth.permission',
            'app.core.models.auth.role',

            'app.core.models.organization.department',
            'app.core.models.organization.employee',
            'app.core.models.organization.organization'
        ]}
    )
    await Tortoise.generate_schemas()


@app.on_event('shutdown')
async def on_shutdown():
    await Tortoise.close_connections()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}
