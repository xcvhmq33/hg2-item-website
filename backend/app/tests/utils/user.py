from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.models import User
from app.schemas import UserCreateSchema, UserUpdateSchema
from app.tests.utils.utils import random_email, random_lower_string


async def create_random_user(db: AsyncSession) -> User:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateSchema(email=email, name=username, password=password)
    user = await crud.create_user(db, user_in)
    return user


async def user_authentication_headers(
    client: AsyncClient, username: str, password: str
) -> dict[str, str]:
    data = {"username": username, "password": password}
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


async def authentication_token_from_username(
    client: AsyncClient, username: str, db: AsyncSession
) -> dict[str, str]:
    password = random_lower_string()
    user = await crud.get_user_by_name(db, username)
    if user is None:
        email = random_email()
        user_in_create = UserCreateSchema(email=email, name=username, password=password)
        user = await crud.create_user(db, user_in_create)
    else:
        user_in_update = UserUpdateSchema(password=password)
        user = await crud.update_user(db, user, user_in_update)

    return await user_authentication_headers(client, username, password)
