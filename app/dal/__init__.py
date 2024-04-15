from sqlalchemy import create_engine as _create_sqlalchemy_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from app.settings import settings


def _create_db() -> Engine:
    engine = _create_sqlalchemy_engine(
        f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}/{settings.database_name}"
    )
    return engine


def get_session() -> sessionmaker:
    return sessionmaker(autocommit=False, autoflush=False, bind=_create_db())
