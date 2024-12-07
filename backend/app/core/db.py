from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.models import Base

engine = create_async_engine(settings.DATABASE_URL)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
