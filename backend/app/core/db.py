from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app import crud
from app.core.config import settings
from app.schemas import UserCreateSchema

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI.unicode_string())


async def init_db(session: AsyncSession) -> None:
    existing_user = await crud.get_user_by_name(session, settings.FIRST_SUPERUSER_NAME)
    if existing_user is None:
        user_in = UserCreateSchema(
            email=settings.FIRST_SUPERUSER_EMAIL,
            name=settings.FIRST_SUPERUSER_NAME,
            password=settings.FIRST_SUPERUSER_PASS,
            is_superuser=True,
        )
        await crud.create_user(session, user_in)
