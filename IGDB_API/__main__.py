from os import getenv

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise

from IGDB_API import DB_URI, PORT, HOST
from IGDB_API.api.api_v1.api import router as api_v1_router


app = FastAPI(
    title="Game API for Project Black Pearl",
    version="0.1.0",
)


class Status(BaseModel):
    message: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/status",
    response_model=Status,
    responses={500: {"model": Status}},
)
async def status():
    return Status(message="OK")


app.include_router(api_v1_router, prefix="/api/v1")


register_tortoise(
    app,
    db_url=DB_URI,
    modules={"models": ["IGDB_API.api.core.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host=HOST, port=PORT)
