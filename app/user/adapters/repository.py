import abc
from app.user.domain import model
from sqlalchemy.orm import Session
from app.user.adapters.orm import users  # Import the users table
from sqlalchemy import insert, select

class AbstractRepository(abc.ABC):

    def __init__(self) -> None:
        self.seen = set()

    def add(self, user: model.User) -> model.User:
        self._add(user)
        self.seen.add(user)
        return user

    def get(self, sku) -> model.User:
        user = self._get(sku)
        if user:
            self.seen.add(user)
        return user

    @abc.abstractmethod
    def _add(self, user: model.User):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, user: model.User):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    
    def __init__(self,session:Session) -> None:
        super().__init__()
        self.session = session

    def _add(self, user: model.User):
        
        stmt = insert(users).values(
            name = user.name,
            password = user.password
        )
        self.session.execute(stmt)
        self.session.commit()
        
        return user
        

    def _get(self, sku):
        return self.session.query(model.User).filter_by(sku=sku).first()
