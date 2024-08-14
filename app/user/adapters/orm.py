from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Text,
)


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(30)),
    Column("password", Text),
)
