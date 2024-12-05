from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    FRONTEND_HOST: str = "http://localhost:5173"
    PROJECT_NAME: str = "Full Stack FastAPI Project"
    API_V1_STR: str = "/api/v1"
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
