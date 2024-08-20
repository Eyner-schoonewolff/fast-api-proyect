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
    Column("last_name", String(30)),
    Column("email", String(40)),
    Column("password", Text),
    Column("document", Integer),
    Column("id_rol", Integer),
)
