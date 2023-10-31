from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.routers import routers_gen


app = FastAPI()

for router in routers_gen():
    app.include_router(router)


@app.get("/")
def index():
    return JSONResponse({"status": "Running ..."})
