from fastapi import APIRouter
from typing import List
from app.user.services.handler import create_user
from app.user.domain import requests
from fastapi.responses import JSONResponse

user = APIRouter()


@user.post("/", response_model=requests.CreateUser, status_code=201)
def create_users(user: requests.CreateUser):

    response = create_user(
        request=requests.CreateUser(name=user.name, password=user.password)
    )

    if response is None:
        return JSONResponse({"user": "no","messague":"No pudo ser registrado."}, status_code=404)

    return JSONResponse({'user':response.dict(),'messague':"registrado correctamente."}, 201)
