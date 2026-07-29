from sqlalchemy.orm import Session

from app.auth.models import User
from app.auth.schemas import UserCreate


class UserRepository:

    @staticmethod
    def create(
        db: Session,
        user: UserCreate,
        hashed_password: str,
    ) -> User:

        db_user = User(
            full_name=user.full_name,
            email=user.email,
            password=hashed_password,
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ):

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int,
    ):

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )