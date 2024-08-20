import pydantic
import hashlib


class CreateUser(pydantic.BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    document: int
    id_rol: int


class Auth(pydantic.BaseModel):
    email: str
    password: str

    @pydantic.field_validator("password")
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
