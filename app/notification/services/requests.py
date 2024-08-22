import pydantic
import hashlib


class CreateNotification(pydantic.BaseModel):
    user_id: int
    title: str
    description: str


class GetNotificationByUserId(pydantic.BaseModel):
    user_id: int
