from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    FRONTEND_HOST: str = "http://localhost:5173"
    PROJECT_NAME: str = "Full Stack FastAPI Project"
    API_V1_STR: str = "/api/v1"
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    TEST_USER_NAME: str
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_NAME: str
    FIRST_SUPERUSER_PASS: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )  # type: ignore[return-value]

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
