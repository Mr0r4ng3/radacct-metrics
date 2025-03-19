from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.RADIUS_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    return SessionLocal()


def get_metadata():
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return metadata
