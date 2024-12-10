from typing import Any, Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import SessionDep
from app.core.security import auth
from app.schemas import Token

router = APIRouter(tags=["login"])


@router.post("/login")
async def login(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Any:
    user = await crud.authenticate(session, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    token = auth.create_access_token(uid=str(user.id))

    return Token(access_token=token)
