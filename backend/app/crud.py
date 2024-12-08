import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models import Item, User
from app.schemas import ItemCreateSchema, UserCreateSchema


# TODO: rename db to session
async def create_item(db: AsyncSession, item_in: ItemCreateSchema) -> Item:
    db_item = Item(
        ingame_id=item_in.ingame_id,
        title_id=item_in.title_id,
        title=item_in.title,
        image_id=item_in.image_id,
        image_url=str(item_in.image_url),
        damage_type=item_in.damage_type,
        rarity=item_in.rarity,
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def create_user(db: AsyncSession, user_in: UserCreateSchema) -> User:
    db_user = User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=get_password_hash(user_in.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_user_by_name(db: AsyncSession, username: str) -> User | None:
    query = select(User).where(User.name == username)
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def get_user_by_email(db: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalars().first()
    return user


async def get_user_by_uuid(db: AsyncSession, uuid: uuid.UUID):
    query = select(User).where(User.id == uuid)
    result = await db.execute(query)
    user = result.scalars().first()
    return user
