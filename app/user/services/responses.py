import pydantic


class ResponseCreateUser(pydantic.BaseModel):
    name: str
    last_name: str
    email: str
    document:int
    id_rol: int
    
    def __init__(self, **user):
        super().__init__(**user)


class ResponseAuth(pydantic.BaseModel):
    id:int
    name: str
    last_name: str
    email: str
    id_rol: int

    def __init__(self, **data):
        super().__init__(**data)
