from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.routers import routers_gen
import uvicorn

app = FastAPI()

for router in routers_gen():
    app.include_router(router)


@app.get("/")
def index():
    return JSONResponse({"status": "Running ..."})


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        proxy_headers=True,
    )
