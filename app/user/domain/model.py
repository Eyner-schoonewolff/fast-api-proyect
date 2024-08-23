import pydantic
from app.user.domain import exceptions
import hashlib
import re
from typing import Optional


class User(pydantic.BaseModel):
    id: Optional[int] = None
    name: str
    password: str
    last_name: str
    email: str
    document: int
    id_rol: int

    @pydantic.field_validator("password")
    def validate_password(cls, password: str) -> str:

        if len(password) < 8:
            raise exceptions.ValidateCharacterPasswordException

        if re.fullmatch(r"[A-Fa-f0-9]{64}", password):
            return password

        # SETEAR HASH
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def authenticate(self, password: str) -> bool:
        return self.password == password

    def verificate_email(self, email: str) -> None:
        if self.email == email:
            raise exceptions.EmailAlreadyExistsException(email)
