from sqlalchemy.orm import Session

from app.core.security import password_hash, verify_password
from app.repositories.user_repository import UserRepository

def register_user( db, user_data):
    existing_user = UserRepository.get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user:
        raise ValueError("User already exists")

    hashed_password = password_hash(user_data.password)

    return UserRepository.create_user(
        db=db,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )

class AuthService:

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str
    ):
        print("AUTH SERVICE db:", type(db))
        user = UserRepository.get_user_by_email(
            db=db,
            email=email,
        )

        # Check whether the user exists
        if user is None:
            return None

        # Check whether the account is active
        if not user.is_active:
            return None

        # Verify the submitted password
        if not verify_password(
            plain_password=password,
            hashed_password=user.hashed_password
        ):
            return None

        # Authentication successful
        return user

