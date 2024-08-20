from fastapi import APIRouter, HTTPException
from app.user.services.handler import UserService
from app.user.services import requests
from fastapi.responses import JSONResponse
from app.user.domain import exceptions
import traceback

user_api_router = APIRouter()


@user_api_router.post("/", response_model=requests.CreateUser, status_code=201)
def create_users(request: requests.CreateUser):

    user_service = UserService()
    try:
        response = user_service.create_user(request=request)

        if response is None:
            return JSONResponse(
                {"user": "no", "detail": "No pudo ser registrado."}, status_code=404
            )

        return JSONResponse(
            {"user": response.model_dump(), "detail": "Registrado correctamente."}, 201
        )

    except exceptions.EmailAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except exceptions.ValidateCharacterPasswordException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_api_router.post("/auth", response_model=requests.Auth, status_code=200)
def auth_user(request: requests.Auth):
    user_service = UserService()
    try:
        user_auth = user_service.auth(request=request)

        if user_auth is None:
            return JSONResponse(
                {
                    "user": user_auth,
                    "auth": "no",
                    "detail": "Email o contraseña incorretcta, pruebe con otras",
                },
                401,
            )

        return JSONResponse(
            {
                "user": user_auth.model_dump(),
                "auth": "ok",
                "detail": "usuario loguedo.",
            },
            200,
        )

    except Exception as e:
        error_traceback = traceback.format_exc()
        raise HTTPException(
            status_code=500, detail=f"Error: {str(e)}, Traceback: {error_traceback}"
        )
