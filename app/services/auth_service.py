
from app.core.security import password_hash
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

    hashed_password = password_hash( user.password )