from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers.auth import authentication


app = FastAPI(debug=True, title="Aberno API")

app.include_router(router=authentication.router, prefix='/api/auth')


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}
