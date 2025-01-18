from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes.routes import router

app = FastAPI()

app.include_router(router, prefix="/data")


@app.get("/")
async def startup():
    return JSONResponse(status_code=200, content="Server Loaded Successfully")
