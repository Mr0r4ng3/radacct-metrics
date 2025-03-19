from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.db.models.base import Model
from app.schemas.users import UserCreate
from app.services.users import UserService

engine = create_engine(
    settings.APP_DATABASE_URI, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db


def init_db():
    Model.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        service = UserService(db=db)

        existing_user = service.get_user_by_username(settings.FIRST_SUPERUSER)

        if existing_user is None:
            service.create(
                UserCreate(
                    username=settings.FIRST_SUPERUSER,
                    full_name="System Admin",
                    password=settings.FIRST_SUPERUSER_PASSWORD,
                )
            )
