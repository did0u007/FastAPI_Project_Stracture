from fastapi import FastAPI
from api.routers import routers_gen


app = FastAPI()

for router in routers_gen():
    app.include_router(router)


@app.get("/", status_code=200)
def index():
    return {"status": "success"}
