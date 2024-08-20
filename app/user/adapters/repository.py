import abc
from app.user.domain import model
from sqlalchemy.orm import Session
from app.user.adapters.orm import users
from sqlalchemy import insert


class UserRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, user: str):
        raise NotImplementedError


class SqlAlchemyRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, user: model.User) -> model.User:
        stmt = insert(users).values(**user.__dict__)
        self.session.execute(stmt)
        self.session.commit()
        return user

    def get(self):
        pass

    def get_by_email(self, email: str) -> model.User | None:
        user = self.session.query(users).filter_by(email=email.strip()).first()
        if user:
            return model.User(**user._asdict())
        return None
