from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.notification.domain import exceptions
import traceback
from app.notification.services.handler import NotificationService
from app.notification.services import requests
import json


notification_api_router = APIRouter()


@notification_api_router.post("/", status_code=201)
def register_notifications(request: requests.CreateNotification):

    notification_service = NotificationService()
    try:
        notification = notification_service.create_notification(request=request)

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
            },
            status_code=201,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@notification_api_router.get("/", status_code=200)
def get_notification(request: requests.GetNotificationByUserId):
    service = NotificationService()
    try:
        notifications = service.get_notifications(request=request)
        if not notifications:
            return JSONResponse(
                {
                    "notification": "no",
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
            },
            status_code=200,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
