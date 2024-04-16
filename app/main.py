from fastapi import FastAPI

from app.routers.auth import authentication
from app.routers import organization, roll_call

from app.settings import settings


app = FastAPI(debug=settings.environment in ['local', 'debug'], title="Aberno API")

app.include_router(router=authentication.router, prefix='/api/auth')
for router in organization.routers:
    app.include_router(router, prefix='/api/organization', tags=['organizations'])
for router in roll_call.routers:
    app.include_router(router=router, prefix='/api')


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}
