from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

metadata = MetaData()

notifications = Table(
    "notification",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("title", String(30)),
    Column("description", Text),
    Column("status", Integer),
    Column("deleted", Integer),
    Column("deleted_date", DateTime),
    Column("creation_date", DateTime),
)

user_notifications = relationship("Notification", backref="users", lazy="dynamic")