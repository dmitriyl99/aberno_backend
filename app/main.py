from fastapi import FastAPI


app = FastAPI(debug=True, title="Aberno API")


@app.get("/app")
def read_main():
    return {"message": "Hello World from main app"}
