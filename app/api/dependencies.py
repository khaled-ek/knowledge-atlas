import uuid

from sqlalchemy.orm import Session
from fastapi import Depends, Request, HTTPException, status
from starlette.responses import RedirectResponse

from app.db.session import sessionLocal
from app.models.user import User
from app.repositories.user_repository import UserRepository

# Database dependency
def get_db():

    db = sessionLocal()

    try:
        yield db

    finally:
        db.close()

# Shared authentication logic
def _load_current_user(
    request: Request,
    db: Session
) -> User | None:

    # 1. Read the user ID from the session
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    # 2. Convert the string into a UUID
    try:
        user_uuid = uuid.UUID(user_id)
    except (ValueError, TypeError, AttributeError):
        request.session.clear()
        return None

    # 3. Retrieve the user from PostgreSQL
    user = UserRepository.get_user_by_id(
        db=db,
        user_id=user_uuid
    )

    # 4. Check whether the user exists and is active
    if user is None or not user.is_active:
        request.session.clear()
        return None

    return user

# Dependency for API endpoints
def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> User:

    user = _load_current_user(request, db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    return user

# Dependency for HTML pages
def get_current_user_for_page(
    request: Request,
    db: Session = Depends(get_db)
) -> User | RedirectResponse:

    user = _load_current_user(request, db)

    if user is None:
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    return user