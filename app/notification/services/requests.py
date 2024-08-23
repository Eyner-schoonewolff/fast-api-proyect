import pydantic
from app.notification.domain import model


class CreateNotification(pydantic.BaseModel):
    user_id: int
    title: str
    description: str


class UpdateNotificationStatus(pydantic.BaseModel):
    id: int
    status: model.NotificationStatus


class UpdateAllNotificationById(pydantic.BaseModel):
    user_id: int
    status: model.NotificationStatus


class GetNotificationByUserId(pydantic.BaseModel):
    user_id: int


class NotificationById(pydantic.BaseModel):
    id: int
