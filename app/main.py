from fastapi import FastAPI
from app.user.entrypoints.app import user
from app.database.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(user, prefix="/api/v1/users", tags=["users"])
