import pydantic

class CreateUser(pydantic.BaseModel):
    name: str
    password: str