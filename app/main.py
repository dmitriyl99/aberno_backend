from fastapi import FastAPI
from tortoise import Tortoise


app = FastAPI(debug=True, title="Aberno API")


@app.on_event('startup')
async def on_startup():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.dal.models.auth.user', 'app.dal.models.auth.permission', 'app.dal.models.auth.role']}
    )
    await Tortoise.generate_schemas()


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}
