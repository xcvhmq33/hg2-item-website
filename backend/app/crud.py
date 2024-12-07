from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item
from app.schemas import ItemCreateSchema


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
