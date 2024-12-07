from typing import Any

from fastapi import APIRouter, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.api.deps import SessionDep
from app.models import Item
from app.schemas import ItemReadSchema

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=list[ItemReadSchema])
async def read_items(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    query = (
        select(Item)
        .offset(skip)
        .limit(limit)
        .options(
            joinedload(Item.properties),
            joinedload(Item.skills),
        )
        .order_by(Item.ingame_id)
    )
    result = await session.execute(query)
    items = result.scalars().unique().all()

    return items


@router.get("/{item_id}", response_model=ItemReadSchema)
async def read_item(session: SessionDep, item_id: int = Path(ge=1)) -> Any:
    query = (
        select(Item)
        .where(Item.ingame_id == item_id)
        .options(
            joinedload(Item.properties),
            joinedload(Item.skills),
        )
    )
    result = await session.execute(query)
    item = result.scalars().unique().first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item
