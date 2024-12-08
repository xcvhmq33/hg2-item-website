from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.core.security import auth, verify_password
from app.schemas import UserLoginSchema

router = APIRouter(tags=["login"])


@router.post("login/")
async def login(session: SessionDep, user_in: UserLoginSchema) -> Any:
    user = await crud.get_user_by_name(session, user_in.name)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=403, detail="Incorrect password")
    token = auth.create_access_token(uid=str(user.id))

    return {"access_token": token}
