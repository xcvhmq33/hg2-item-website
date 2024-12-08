from typing import Any

from fastapi import APIRouter, HTTPException, Path
from sqlalchemy import select

from app import crud
from app.api.deps import SessionDep
from app.models import User
from app.schemas import UserCreateSchema, UserReadSchema, UserRegisterSchema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserReadSchema])
async def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    query = select(User).offset(skip).limit(limit).order_by(User.name)
    result = await session.execute(query)
    users = result.scalars().all()

    return users


@router.get("/{username}", response_model=UserReadSchema)
async def read_user(session: SessionDep, username: str = Path(max_length=32)) -> Any:
    user = await crud.get_user_by_name(session, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/", response_model=UserReadSchema)
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
    user_in = UserCreateSchema(**user_in.__dict__)
    user = await crud.create_user(session, user_in)

    return user
