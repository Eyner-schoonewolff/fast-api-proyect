from fastapi import APIRouter, HTTPException, Depends, Path
from fastapi.responses import JSONResponse
from app.notification.services.handler import NotificationService
from app.notification.services import requests
from app.jwt.security import jwt_config
from fastapi_jwt import JwtAccessBearer


notification_api_router = APIRouter()


@notification_api_router.post("/", status_code=201)
def register_notifications(
    request: requests.CreateNotification,
    credentials: JwtAccessBearer = Depends(jwt_config.get_access_security()),
):

    service = NotificationService()
    try:
        notification = service.create_notification(request=request)

        if not notification:

            return JSONResponse(
                {
                    "notification": "no",
                    "detail": "hubo problemas al registrar la notificacion",
                },
                status_code=400,
            )

        return JSONResponse(
            {
                "notification": notification.model_dump(by_alias=True),
                "detail": "Registrado correctamente.",
                "credentials": credentials.subject,
            },
            status_code=201,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@notification_api_router.get("/all/{user_id}", status_code=200)
def get_notifications(
    user_id: int = Path(..., title="id del usuario"),
    credentials: JwtAccessBearer = Depends(jwt_config.get_access_security()),
):
    service = NotificationService()
    try:
        notifications = service.get_notifications(user_id=user_id)
        if not notifications:
            return JSONResponse(
                {
                    "notifications": notifications,
                    "detail": "Este usuario no tiene notificaciones registradas",
                },
                status_code=200,
            )
        return JSONResponse(
            {
                "notifications": [
                    notification.model_dump() for notification in notifications
                ],
                "detail": "ok",
                "credentials": credentials.subject,
            },
            status_code=200,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@notification_api_router.get("/{id}", status_code=200)
def get_notification(
    id: int = Path(..., title="id de la notificacion"),
    credentials: JwtAccessBearer = Depends(jwt_config.get_access_security()),
):
    service = NotificationService()
    try:
        notification = service.get_notification(id=id)

        if not notification:
            return JSONResponse(
                {
                    "notification": "no",
                    "detail": "Este usuario no tiene notificaciones disponibles.",
                },
                status_code=404,
            )
        return JSONResponse(
            {
                "notification": notification.model_dump(by_alias=True),
                "detail": "ok",
                "credentials": credentials.subject,
            },
            status_code=200,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@notification_api_router.put("/status", status_code=200)
def update_notification_status(
    request: requests.UpdateNotificationStatus,
    credentials: JwtAccessBearer = Depends(jwt_config.get_access_security()),
):
    service = NotificationService()
    try:
        service.update_notification_status(request=request)
        return JSONResponse(
            {
                "notification": "Estado actualizado correctamente",
                "detail": "ok",
                "credentials": credentials.subject,
            },
            status_code=200,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@notification_api_router.put("/all_status", status_code=200)
def read_all_status_notifications(
    request: requests.UpdateAllNotificationById,
    credentials: JwtAccessBearer = Depends(jwt_config.get_access_security()),
):
    service = NotificationService()
    try:

        service.update_all_notifications(request=request)
        return JSONResponse(
            {
                "notification": "Estados actualizados correctamente.",
                "detail": "ok",
                "credentials": credentials.subject,
            },
            status_code=200,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@notification_api_router.put("/deleted", status_code=200)
def deleted_notification(
    request: requests.NotificationById,
    credentials: JwtAccessBearer = Depends(jwt_config.get_access_security()),
):
    service = NotificationService()
    try:
        service.deleted_notification(request=request)
        return JSONResponse(
            {
                "notification": "Notificacion eliminada correctamente.",
                "detail": "ok",
                "credentials": credentials.subject,
            },
            status_code=200,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
