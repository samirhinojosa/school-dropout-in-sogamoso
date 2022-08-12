from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from .settings import get_settings


# Runtime Environment Configuration
settings = get_settings()


# Generate Database URL
DATABASE_URL = f"{settings.DATABASE_DIALECT}://{settings.DATABASE_USERNAME}:\
                    {settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:\
                    {settings.DATABASE_PORT}/{settings.DATABASE_NAME}"


Engine = create_engine(
    DATABASE_URL
)


SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


# Dependency
def get_db():
    """
    Independent database session/connection per request, 
    who uses the same session through all the request 
    and then close it after the request is finished.
    """
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()