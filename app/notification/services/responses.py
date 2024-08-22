import pydantic
from datetime import datetime
from typing import List, Optional
from app.notification.domain import model


class ResponseNotification(pydantic.BaseModel):
    user_id: int
    title: str
    description: str
    status: int
    deleted: int
    deleted_date: str | None
    creation_date: str

    def __init__(self, **data):
        super().__init__(**data)


class NotificationUser(pydantic.BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    status: int
    deleted: int
    deleted_date: datetime | None
    creation_date: datetime
    user_name: str
    user_last_name: str
