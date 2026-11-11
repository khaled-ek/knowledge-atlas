
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.user import User

class UserRepository:

    @staticmethod
    def get_user_by_email(
        db: Session,
        email: str
    ) -> User | None:

        """
        Retrieves a user by email
        :param db: The database session
        :param email: The user email address
        :return: The retrieved user
        """

        statement = select(User).where(
            User.email == email
        )

        return db.scalar(statement)

    @staticmethod
    def create_user(
        db: Session,
        full_name: str,
        email: str,
        hashed_password: str,
        is_active: bool
    ) -> User:

        """
        Create and save a new user
        :param db: The database session
        :param full_name: The full name of the user
        :param email: The email address
        :param hashed_password: The hashed password of the user
        :param is_active:
        :return:
        """

        new_user = User(
            name=full_name,
            email=email,
            hashed_password=hashed_password,
            is_active=True
        )