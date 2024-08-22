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


class BaseSerializer(pydantic.BaseModel):
    @pydantic.field_serializer("creation_date", check_fields=False, when_used="always")
    def serialize_creation_date(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")

    @pydantic.field_serializer("deleted_date", check_fields=False, when_used="always")
    def serialize_deleted_date(self, value: Optional[datetime]) -> Optional[str]:
        return value.strftime("%Y-%m-%d %H:%M:%S") if value is not None else None


class Notification(BaseSerializer):
    id: Optional[int] = None
    user_id: int
    title: str
    description: str
    status: NotificationStatus = NotificationStatus.ACTIVE.value
    deleted: NotificationIsDeleted = NotificationIsDeleted.ACTIVE.value
    deleted_date: Optional[datetime] = None
    creation_date: datetime = pydantic.Field(default_factory=datetime.now)


class NotificationUser(BaseSerializer):
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
