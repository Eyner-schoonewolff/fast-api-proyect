from app.notification.domain import model
from app.notification.adapters import repository
from app.notification.services import requests, responses
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.database.db import engine


class NotificationService:
    def __init__(self) -> None:

        self.sessionLocal = sessionmaker(bind=engine)

    def create_notification(
        self, request: requests.CreateNotification
    ) -> responses.ResponseNotification:

        session = self.sessionLocal()

        notitfication = model.Notification(
            user_id=request.user_id,
            title=request.title,
            description=request.description,
        )

        try:
            repo = repository.SqlAlchemyRepository(session=session)
            create_notification = repo.add(notification=notitfication)
        except SQLAlchemyError as e:
            session.rollback()
            raise Exception(f"Problema de: {str(e)}")
        finally:
            session.close()

        return responses.ResponseNotification(**create_notification.model_dump())

    def get_notifications(
        self, request: requests.GetNotificationByUserId
    ) -> list[responses.NotificationUser]:
        with self.sessionLocal() as session:
            repo = repository.SqlAlchemyRepository(session=session)
            notifications = repo.get_by_user(id=request.user_id)
        return notifications
