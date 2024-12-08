from datetime import timedelta

from authx import AuthX, AuthXConfig
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

authx_config = AuthXConfig(
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY="SECRET_KEY",
    JWT_TOKEN_LOCATION=["headers"],
)

auth = AuthX(authx_config)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
