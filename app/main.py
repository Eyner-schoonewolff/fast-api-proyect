from fastapi import FastAPI
from app.user.entrypoints.app import user_api_router
from app.notification.entrypoints.app import notification_api_router
from app.database.db import metadata, database, engine
import fastapi.middleware.cors as cors

metadata.create_all(engine)

app = FastAPI()



app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todas las cabeceras
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(user_api_router, prefix="/api/v1/user", tags=["user"])
app.include_router(
    notification_api_router, prefix="/api/v1/notification", tags=["notification"]
)
