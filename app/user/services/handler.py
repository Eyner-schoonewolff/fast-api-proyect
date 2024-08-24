from app.user.domain import model
from app.user.adapters import repository
from app.user.services import requests, responses
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.database.db import engine


class UserService:
    def __init__(self) -> None:
        self.sessionLocal = sessionmaker(bind=engine)

    # authenticate
    def auth(self, request: requests.Auth) -> responses.ResponseAuth:

        session = self.sessionLocal()

        try:
            repo = repository.SqlAlchemyRepository(session=session)
            user = repo.get_by_email(email=request.email)

            if not user:
                return None

            if not user.authenticate(request.password) or not user:
                return None

        except SQLAlchemyError as e:
            raise Exception(f"Problema de : {str(e)}")

        finally:
            session.close()

        return responses.ResponseAuth(**user.model_dump())

    def create_user(self, request: requests.CreateUser) -> responses.ResponseCreateUser:

        user = model.User(**request.model_dump())

        try:

            session = self.sessionLocal()
            repo = repository.SqlAlchemyRepository(session=session)

            if repo.get_by_email(email=user.email):
                user.verificate_email(email=request.email)

            user_created = repo.add(user=user)

        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(
                f"Error al realizar procedimineto de registrar el usuario en la base de datos: {str(e)}"
            )
        finally:
            session.close()

        return responses.ResponseCreateUser(**user_created.model_dump())
