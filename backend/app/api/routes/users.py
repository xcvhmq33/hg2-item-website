from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import func, select

from app import crud
from app.api.deps import SessionDep, get_current_active_superuser
from app.models import User
from app.schemas import (
    UserCreateSchema,
    UserReadSchema,
    UserRegisterSchema,
    UsersReadSchema,
    UserUpdateSchema,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UsersReadSchema,
)
async def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_query = select(func.count()).select_from(User)
    count_result = await session.execute(count_query)
    count = count_result.scalars().one()
    users_query = select(User).offset(skip).limit(limit).order_by(User.name)
    users_result = await session.execute(users_query)
    users = users_result.scalars().all()

    return UsersReadSchema(data=users, count=count)


@router.get(
    "/{username}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserReadSchema,
)
async def read_user(session: SessionDep, username: str = Path(max_length=32)) -> Any:
    user = await crud.get_user_by_name(session, username)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="The user with this name does not exist in the system",
        )

    return user


@router.post(
    "/",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserReadSchema,
)
async def create_user(session: SessionDep, user_in: UserCreateSchema) -> Any:
    existing_user = await crud.get_user_by_name(session, user_in.name)
    if existing_user is not None:
        raise HTTPException(
            status_code=409, detail="User with this name already exists"
        )
    existing_user = await crud.get_user_by_email(session, user_in.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=409, detail="User with this email already exists"
        )
    user = await crud.create_user(session, user_in)

    return user


@router.post("/signup", response_model=UserReadSchema)
async def register_user(session: SessionDep, user_in: UserRegisterSchema) -> Any:
    existing_user = await crud.get_user_by_name(session, user_in.name)
    if existing_user is not None:
        raise HTTPException(
            status_code=409, detail="User with this name already exists"
        )
    existing_user = await crud.get_user_by_email(session, user_in.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=409, detail="User with this email already exists"
        )
    user_create = UserCreateSchema(**user_in.__dict__)
    user = await crud.create_user(session, user_create)

    return user


@router.patch(
    "/{username}",
    dependencies=[Depends(get_current_active_superuser)],
    response_model=UserReadSchema,
)
async def update_user(
    session: SessionDep,
    username: str,
    user_in: UserUpdateSchema,
) -> Any:
    db_user = await crud.get_user_by_name(session, username)
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="The user with this name does not exist in the system",
        )
    if user_in.email:
        existing_user = await crud.get_user_by_email(
            session=session, email=user_in.email
        )
        if existing_user and existing_user.name != username:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )
    if user_in.name:
        existing_user = await crud.get_user_by_name(
            session=session, username=user_in.name
        )
        if existing_user and existing_user.name != username:
            raise HTTPException(
                status_code=409, detail="User with this name already exists"
            )
    updated_user = await crud.update_user(
        session=session, db_user=db_user, user_in=user_in
    )
    return updated_user
