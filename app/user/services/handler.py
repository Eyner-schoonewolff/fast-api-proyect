from app.user.domain import requests, model
from app.user.adapters import repository
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.database.db import engine

SessionLocal = sessionmaker(bind=engine)

def create_user(request: requests.CreateUser) -> model.User | None:

    user = model.User(
        name=request.name,
        password=request.password,
    )

    if user.is_secure_password():

        session = SessionLocal()

        try:
            repo = repository.SqlAlchemyRepository(session=session)
            
            try:

                insertUser = repo._add(user=user)
                return insertUser

            except SQLAlchemyError as e:
                session.rollback()
                raise Exception(
                    f"Error al insertar el usuario en la base de datos: {str(e)}"
                )

        finally:
            session.close()

    return None
