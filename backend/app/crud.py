import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models import Item, User
from app.schemas import ItemCreateSchema, UserCreateSchema


async def create_item(session: AsyncSession, item_in: ItemCreateSchema) -> Item:
    db_item = Item(
        ingame_id=item_in.ingame_id,
        title_id=item_in.title_id,
        title=item_in.title,
        image_id=item_in.image_id,
        image_url=str(item_in.image_url),
        damage_type=item_in.damage_type,
        rarity=item_in.rarity,
    )
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def create_user(session: AsyncSession, user_in: UserCreateSchema) -> User:
    db_user = User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=get_password_hash(user_in.password),
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_user_by_name(session: AsyncSession, username: str) -> User | None:
    query = select(User).where(User.name == username)
    result = await session.execute(query)
    user = result.scalars().first()
    return user


async def get_user_by_email(session: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalars().first()
    return user


async def get_user_by_uuid(session: AsyncSession, uuid: uuid.UUID):
    query = select(User).where(User.id == uuid)
    result = await session.execute(query)
    user = result.scalars().first()
    return user

async def authenticate(session: AsyncSession, name: str, password: str) -> User | None:
    db_user = await get_user_by_name(session, name)
    if db_user is None:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user
