from sqlalchemy.orm import Session

from app.auth.repository import UserRepository
from app.auth.schemas import (
    Token,
    UserCreate,
    UserLogin,
)
from app.auth.security import (
    create_access_token,
    hash_password,
    verify_password,
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        user: UserCreate,
    ):

        existing_user = UserRepository.get_by_email(
            db,
            user.email,
        )

        if existing_user:
            raise ValueError(
                "Email already registered."
            )

        hashed_password = hash_password(
            user.password
        )

        return UserRepository.create(
            db,
            user,
            hashed_password,
        )

    @staticmethod
    def login(
        db: Session,
        credentials: UserLogin,
    ) -> Token:

        user = UserRepository.get_by_email(
            db,
            credentials.email,
        )

        if not user:
            raise ValueError(
                "Invalid email or password."
            )

        if not verify_password(
            credentials.password,
            user.password,
        ):
            raise ValueError(
                "Invalid email or password."
            )

        access_token = create_access_token(
            {
                "sub": user.email,
                "role": user.role,
            }
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )