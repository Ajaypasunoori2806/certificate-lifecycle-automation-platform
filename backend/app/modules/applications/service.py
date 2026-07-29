from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.applications.repository import ApplicationRepository
from app.modules.applications.schemas import (
    ApplicationCreate,
    ApplicationUpdate,
)


class ApplicationService:

    @staticmethod
    def create_application(
        db: Session,
        application: ApplicationCreate,
    ):
        applications = ApplicationRepository.get_all(db)

        for app in applications:
            if (
                app.application_name.lower()
                == application.application_name.lower()
            ):
                raise HTTPException(
                    status_code=400,
                    detail="Application already exists.",
                )

        return ApplicationRepository.create(db, application)

    @staticmethod
    def get_all_applications(db: Session):
        return ApplicationRepository.get_all(db)

    @staticmethod
    def get_application(
        db: Session,
        application_id: int,
    ):
        application = ApplicationRepository.get_by_id(
            db,
            application_id,
        )

        if application is None:
            raise HTTPException(
                status_code=404,
                detail="Application not found.",
            )

        return application

    @staticmethod
    def update_application(
        db: Session,
        application_id: int,
        application: ApplicationUpdate,
    ):
        db_application = ApplicationRepository.get_by_id(
            db,
            application_id,
        )

        if db_application is None:
            raise HTTPException(
                status_code=404,
                detail="Application not found.",
            )

        return ApplicationRepository.update(
            db,
            db_application,
            application,
        )

    @staticmethod
    def delete_application(
        db: Session,
        application_id: int,
    ):
        db_application = ApplicationRepository.get_by_id(
            db,
            application_id,
        )

        if db_application is None:
            raise HTTPException(
                status_code=404,
                detail="Application not found.",
            )

        ApplicationRepository.delete(
            db,
            db_application,
        )

        return {
            "message": "Application deleted successfully."
        }