import abc
from app.notification.domain import model
from sqlalchemy.orm import Session
from app.notification.adapters import orm
from app.user.adapters import orm as user_orm
from sqlalchemy import insert, select, join, and_
from datetime import datetime


class NotificationRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, notification):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_user(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def read_all(self):
        raise NotImplementedError

    @abc.abstractmethod
    def deleted(self, id: int):
        raise NotImplementedError


class SqlAlchemyRepository(NotificationRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, notification: model.Notification) -> model.Notification:
        notification_data = notification.model_dump(by_alias=True)
        stmt = insert(orm.notifications).values(notification_data)
        self.session.execute(stmt)
        self.session.commit()
        return notification

    def get_by_user(self, id: int) -> list[model.NotificationUser]:
        join_condition = join(
            orm.notifications,
            user_orm.users,
            orm.notifications.c.user_id == user_orm.users.c.id,
        )
        query = (
            select(
                orm.notifications.c.id,
                orm.notifications.c.user_id,
                orm.notifications.c.title,
                orm.notifications.c.description,
                orm.notifications.c.status,
                orm.notifications.c.deleted,
                orm.notifications.c.deleted_date,
                orm.notifications.c.creation_date,
                user_orm.users.c.name.label("user_name"),
                user_orm.users.c.last_name.label("user_last_name"),
            )
            .select_from(join_condition)
            .where(
                and_(
                    orm.notifications.c.user_id == id,
                    orm.notifications.c.deleted
                    == model.NotificationIsDeleted.ACTIVE.value,
                )
            )
        )

        user_notifications = self.session.execute(query).mappings().all()
        return [
            model.NotificationUser.model_validate(user) for user in user_notifications
        ]

    def update(self, id: int) -> model.Notification:
        pass

    def read(self, id: int) -> model.Notification:
        pass

    def read_all(self) -> model.Notification:
        pass

    def deleted(self, id: int) -> model.Notification:
        pass
