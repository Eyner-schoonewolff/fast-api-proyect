import abc
from app.notification.domain import model
from sqlalchemy.orm import Session
from app.notification.adapters import orm
from app.user.adapters import orm as user_orm
import sqlalchemy as sql
import datetime


class NotificationRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, notification):
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_user(self, id: int):
        raise NotImplementedError

    @abc.abstractmethod
    def update_status(self, id: int, status: int):
        raise NotImplementedError

    @abc.abstractmethod
    def update_all_status(self, user_id: int, status: int):
        raise NotImplementedError

    @abc.abstractmethod
    def deleted(self, id: int):
        raise NotImplementedError


class SqlAlchemyRepository(NotificationRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, notification: model.Notification) -> model.Notification:
        notification_data = notification.model_dump(by_alias=True)
        stmt = sql.insert(orm.notifications).values(notification_data)
        self.session.execute(stmt)
        self.session.commit()
        return notification

    def get_by_notification(self, id: int) -> model.NotificationUser:
        join_condition = sql.join(
            orm.notifications,
            user_orm.users,
            orm.notifications.c.user_id == user_orm.users.c.id,
        )
        query = (
            sql.select(
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
                sql.and_(
                    orm.notifications.c.id == id,
                    orm.notifications.c.deleted
                    == model.NotificationIsDeleted.ACTIVE.value,
                )
            )
        )
        user_notification = self.session.execute(query).mappings().first()
        return (
            None
            if not user_notification
            else model.NotificationUser.model_validate(user_notification)
        )

    def get_by_user(self, user_id: int) -> list[model.NotificationUser]:
        join_condition = sql.join(
            orm.notifications,
            user_orm.users,
            orm.notifications.c.user_id == user_orm.users.c.id,
        )
        query = (
            sql.select(
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
                sql.and_(
                    orm.notifications.c.user_id == user_id,
                    orm.notifications.c.deleted == model.NotificationIsDeleted.ACTIVE.value,
                )
            )
        )

        user_notifications = self.session.execute(query).mappings().all()
        return [
            model.NotificationUser.model_validate(user) for user in user_notifications
        ]

    def read(self, id: int, status: int) -> int:
        stmt = (
            orm.notifications.update()
            .where(orm.notifications.c.id == id)
            .values(
                {orm.notifications.c.status: model.NotificationStatus(status).value}
            )
        )

        read = self.session.execute(stmt)
        self.session.commit()
        return read.rowcount

    def update_status(self, id: int, status: int) -> int:
        stmt = (
            orm.notifications.update()
            .where(
                orm.notifications.c.id == id,
                orm.notifications.c.deleted == model.NotificationIsDeleted.ACTIVE.value,
            )
            .values(
                {
                    orm.notifications.c.status: model.NotificationStatus(status).value,
                }
            )
        )

        self.session.execute(stmt)
        self.session.commit()

    def update_all_status(self, user_id: int, status: int) -> None:
        stmt = (
            orm.notifications.update()
            .where(
                orm.notifications.c.user_id == user_id,
                orm.notifications.c.deleted == model.NotificationIsDeleted.ACTIVE.value,
            )
            .values(
                {orm.notifications.c.status: model.NotificationStatus(status).value}
            )
        )
        self.session.execute(stmt)
        self.session.commit()

    def deleted(self, id: int) -> None:

        stmt = (
            orm.notifications.update()
            .where(orm.notifications.c.id == id)
            .values(
                {
                    orm.notifications.c.deleted: model.NotificationIsDeleted.INACTIVE.value,
                    orm.notifications.c.deleted_date: datetime.datetime.now(),
                }
            )
        )
        self.session.execute(stmt)
        self.session.commit()
