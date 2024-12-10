from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.models import Base
from app.schemas import UserCreateSchema
from app import crud
from sqlalchemy.ext.asyncio import AsyncSession

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI.unicode_string())


async def init_db(session: AsyncSession) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        user = await crud.get_user_by_name(session, settings.FIRST_SUPERUSER_NAME)
        if user is None:
            user_in = UserCreateSchema(
                email=settings.FIRST_SUPERUSER_EMAIL,
                name=settings.FIRST_SUPERUSER_NAME,
                password=settings.FIRST_SUPERUSER_PASS,
                is_superuser=True,
            )
            user = await crud.create_user(session, user_in)
