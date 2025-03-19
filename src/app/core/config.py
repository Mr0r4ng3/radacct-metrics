from pathlib import Path
from typing import Literal

from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 15

    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIROMENT: Literal["development", "production"] = "development"
    PROJECT_NAME: str
    FIRST_SUPERUSER: str = "admin"
    FIRST_SUPERUSER_PASSWORD: str

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASS: str
    MYSQL_DB: str

    @property
    def RADIUS_DATABASE_URI(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme="mysql+mysqlconnector",
                username=self.MYSQL_USER,
                password=self.MYSQL_PASS,
                host=self.MYSQL_HOST,
                port=self.MYSQL_PORT,
                path=self.MYSQL_DB,
            )
        )

    @property
    def APP_DATABASE_URI(self) -> str:
        return f"sqlite:///{ROOT_DIR}/db.sqlite3"


settings = Settings()
