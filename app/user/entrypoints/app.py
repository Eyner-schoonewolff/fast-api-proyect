from fastapi import APIRouter, HTTPException, Depends
from app.user.services.handler import UserService
from app.user.services import requests
from fastapi.responses import JSONResponse
from app.user.domain import exceptions
from app.jwt.security import jwt_config
import traceback

user_api_router = APIRouter()


@user_api_router.post("/", response_model=requests.CreateUser, status_code=201)
def create_users(request: requests.CreateUser):
    user_service = UserService()
    try:
        response = user_service.create_user(request=request)

        if not response:
            return JSONResponse(
                {
                    "user": None,
                    "response": "no",
                    "detail": "No pudo ser registrado.",
                },
                status_code=404,
            )

        return JSONResponse(
            {
                "user": response.model_dump(),
                "response": "ok",
                "detail": "Registrado correctamente.",
            },
            201,
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

        if not user_auth:
            return JSONResponse(
                {
                    "user": user_auth,
                    "auth": "no",
                    "token": None,
                    "detail": "Email o contraseña incorrecta, pruebe con otras",
                },
                401,
            )

        user_auth = user_auth.model_dump()
        token = jwt_config.access_security.create_access_token(subject=user_auth)

        return JSONResponse(
            {
                "user": user_auth,
                "auth": "ok",
                "token": token,
                "detail": "Usuario logueado.",
            },
            200,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}, Traceback: {traceback.format_exc()}",
        )
