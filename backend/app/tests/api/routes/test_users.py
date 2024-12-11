import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.config import settings
from app.core.security import verify_password
from app.schemas import UserCreateSchema
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_read_user(
    client: AsyncClient, superuser_token_headers: dict[str, str], db: AsyncSession
) -> None:
    user = await create_random_user(db)
    user_id = user.name
    r = await client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = await crud.get_user_by_email(db, user.email)
    assert existing_user is not None
    assert existing_user.email == api_user["email"]
    assert existing_user.name == api_user["name"]


@pytest.mark.asyncio
async def test_read_user_current_user(client: AsyncClient, db: AsyncSession) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateSchema(email=email, name=username, password=password)
    await crud.create_user(db, user_in)

    login_data = {
        "username": username,
        "password": password,
    }
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = await client.get(
        f"{settings.API_V1_STR}/users/{username}",
        headers=headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = await crud.get_user_by_name(db, username)
    assert existing_user
    assert existing_user.email == api_user["email"]
    assert existing_user.name == api_user["name"]


@pytest.mark.asyncio
async def test_read_user_permissions_error(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
) -> None:
    r = await client.get(
        f"{settings.API_V1_STR}/users/{random_lower_string()}",
        headers=normal_user_token_headers,
    )
    assert r.status_code == 403
    assert r.json() == {"detail": "The user doesn't have enough privileges"}


@pytest.mark.asyncio
async def test_read_users(
    client: AsyncClient, superuser_token_headers: dict[str, str], db: AsyncSession
) -> None:
    await create_random_user(db)
    await create_random_user(db)
    r = await client.get(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
    )
    api_users = r.json()
    assert len(api_users["data"]) >= 2
    assert "count" in api_users
    assert api_users["count"] == len(api_users["data"])
    for item in api_users["data"]:
        assert "email" in item
        assert "name" in item


@pytest.mark.asyncio
async def test_create_user_by_normal_user(
    client: AsyncClient, normal_user_token_headers: dict[str, str]
) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": username, "password": password}
    r = await client.post(
        f"{settings.API_V1_STR}/users/",
        headers=normal_user_token_headers,
        json=data,
    )
    assert r.status_code == 403


@pytest.mark.asyncio
async def test_create_user_by_superuser(
    client: AsyncClient, superuser_token_headers: dict[str, str], db: AsyncSession
) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": username, "password": password}
    r = await client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = await crud.get_user_by_name(db, username)
    assert user
    assert user.email == created_user["email"]
    assert user.name == created_user["name"]


@pytest.mark.asyncio
async def test_create_user_existing_name(
    client: AsyncClient, superuser_token_headers: dict[str, str], db: AsyncSession
) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateSchema(email=email, name=username, password=password)
    await crud.create_user(db, user_in)
    data = {"email": "new_email@example.com", "name": username, "password": password}
    r = await client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this name already exists"
    assert "_id" not in created_user


@pytest.mark.asyncio
async def test_create_user_existing_email(
    client: AsyncClient, superuser_token_headers: dict[str, str], db: AsyncSession
) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateSchema(email=email, name=username, password=password)
    await crud.create_user(db, user_in)
    data = {"email": email, "name": "new_username", "password": password}
    r = await client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    created_user = r.json()
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this email already exists"
    assert "_id" not in created_user


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient, db: AsyncSession) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    data = {"email": email, "name": username, "password": password}
    r = await client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data,
    )
    assert r.status_code == 200
    created_user = r.json()
    assert created_user["email"] == email
    assert created_user["name"] == username

    user_db = await crud.get_user_by_name(db, username)
    assert user_db
    assert user_db.email == email
    assert user_db.name == username
    assert verify_password(password, user_db.hashed_password)


@pytest.mark.asyncio
async def test_register_user_already_exists_name(client: AsyncClient) -> None:
    email = random_email()
    password = random_lower_string()
    data = {
        "email": email,
        "name": settings.FIRST_SUPERUSER_NAME,
        "password": password,
    }
    r = await client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this name already exists"


@pytest.mark.asyncio
async def test_register_user_already_exists_email(client: AsyncClient) -> None:
    username = random_lower_string()
    password = random_lower_string()
    data = {
        "email": settings.FIRST_SUPERUSER_EMAIL,
        "name": username,
        "password": password,
    }
    r = await client.post(
        f"{settings.API_V1_STR}/users/signup",
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this email already exists"


@pytest.mark.asyncio
async def test_update_user(
    client: AsyncClient, superuser_token_headers: dict[str, str], db: AsyncSession
) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateSchema(email=email, name=username, password=password)
    user = await crud.create_user(db, user_in)

    data = {"email": "Updated_email@example.com"}
    r = await client.patch(
        f"{settings.API_V1_STR}/users/{user.name}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 200
    updated_user = r.json()

    assert updated_user["email"] == "Updated_email@example.com"

    user_db = await crud.get_user_by_name(db, username)
    await db.refresh(user_db)
    assert user_db
    assert user_db.email == "Updated_email@example.com"


@pytest.mark.asyncio
async def test_update_user_not_exists(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"name": "Updated_name"}
    r = await client.patch(
        f"{settings.API_V1_STR}/users/{random_lower_string()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 404
    assert r.json()["detail"] == "The user with this name does not exist in the system"


@pytest.mark.asyncio
async def test_update_user_name_exists(
    client: AsyncClient, superuser_token_headers: dict[str, str], db: AsyncSession
) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateSchema(email=email, name=username, password=password)
    user = await crud.create_user(db, user_in)

    email2 = random_email()
    username2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreateSchema(email=email2, name=username2, password=password2)
    user2 = await crud.create_user(db, user_in2)

    data = {"name": user2.name}
    r = await client.patch(
        f"{settings.API_V1_STR}/users/{user.name}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this name already exists"


@pytest.mark.asyncio
async def test_update_user_email_exists(
    client: AsyncClient, superuser_token_headers: dict[str, str], db: AsyncSession
) -> None:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreateSchema(email=email, name=username, password=password)
    user = await crud.create_user(db, user_in)

    email2 = random_email()
    username2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreateSchema(email=email2, name=username2, password=password2)
    user2 = await crud.create_user(db, user_in2)

    data = {"email": user2.email}
    r = await client.patch(
        f"{settings.API_V1_STR}/users/{user.name}",
        headers=superuser_token_headers,
        json=data,
    )
    assert r.status_code == 409
    assert r.json()["detail"] == "User with this email already exists"
