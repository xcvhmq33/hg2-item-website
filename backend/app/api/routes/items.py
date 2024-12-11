from typing import Any

from fastapi import APIRouter, HTTPException, Path
from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from app.api.deps import SessionDep
from app.models import Item
from app.schemas import ItemReadSchema, ItemsReadSchema

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=ItemsReadSchema)
async def read_items(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_query = select(func.count()).select_from(Item)
    count_result = await session.execute(count_query)
    count = count_result.scalars().one()
    items_query = (
        select(Item)
        .offset(skip)
        .limit(limit)
        .options(
            joinedload(Item.properties),
            joinedload(Item.skills),
        )
        .order_by(Item.ingame_id)
    )
    items_result = await session.execute(items_query)
    items = items_result.scalars().unique().all()

    return ItemsReadSchema(data=items, count=count)


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
