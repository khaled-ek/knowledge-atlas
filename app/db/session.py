from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Creating the database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.APP_ENV == 'development'
)

# Creating a session factory
sessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)