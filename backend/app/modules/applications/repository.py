from sqlalchemy.orm import Session

from app.modules.applications.models import Application
from app.modules.applications.schemas import (
    ApplicationCreate,
    ApplicationUpdate,
)


class ApplicationRepository:

    @staticmethod
    def create(db: Session, application: ApplicationCreate) -> Application:
        db_application = Application(**application.model_dump())

        db.add(db_application)
        db.commit()
        db.refresh(db_application)

        return db_application

    @staticmethod
    def get_all(db: Session):
        return db.query(Application).all()

    @staticmethod
    def get_by_id(db: Session, application_id: int):
        return (
            db.query(Application)
            .filter(Application.id == application_id)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        db_application: Application,
        application: ApplicationUpdate,
    ):

        update_data = application.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_application, key, value)

        db.commit()
        db.refresh(db_application)

        return db_application

    @staticmethod
    def delete(
        db: Session,
        db_application: Application,
    ):
        db.delete(db_application)
        db.commit()