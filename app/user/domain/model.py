import pydantic

class User(pydantic.BaseModel):
    
    name:str
    password: str

    def is_secure_password(self) -> bool:
        return len(self.password) > 8