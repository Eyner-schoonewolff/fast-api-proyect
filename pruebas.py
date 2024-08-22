from typing import Optional
from datetime import datetime
import pydantic
import enum


class IntEnum(int, enum.Enum):
    def __repr__(self) -> int:
        return int.__repr__(self.value)


class NotificationStatus(IntEnum):
    ACTIVE = 1
    INACTIVE = 2


class NotificationIsDeleted(IntEnum):
    ACTIVE = 1
    INACTIVE = 2


class Notification(pydantic.BaseModel):
    id: int | None = None
    user_id: int
    title: str
    description: str
    status: NotificationStatus = NotificationStatus.ACTIVE
    deleted: NotificationIsDeleted = NotificationIsDeleted.ACTIVE
    deleted_date: datetime | None = None
    creation_date: datetime = pydantic.Field(
        default=datetime.now(),
    )

    @pydantic.field_serializer("creation_date", when_used="always")
    def serialize_creation_date(self, value: datetime) -> str:
        return value.strftime("%d-%m-%Y %H:%M:%S")

    @pydantic.field_serializer("deleted_date", when_used="always")
    def serialize_deleted_date(self, value: Optional[datetime]) -> Optional[str]:
        return value.strftime("%d-%m-%Y %H:%M:%S") if value is not None else None


# Ejemplo de uso
data = {
    "user_id": 1,
    "title": "Pelicula",
    "description": "Pelicula basada en los alimentos del futuro y sus procesos",
}

notification = Notification(**data)

# Para aplicar la serialización personalizada
print(notification.dict(by_alias=True))
