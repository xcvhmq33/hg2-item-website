import random

from hg2_item_parser.enums import DamageType
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.models import Item
from app.schemas import ItemCreateSchema
from app.tests.utils.utils import random_lower_string


async def create_random_item(db: AsyncSession) -> Item:
    ingame_id = random.randint(1, 5000)
    title_id = random.randint(1, 5000)
    title = random_lower_string()
    image_id = random.randint(1, 5000)
    image_url = f"http://example.com/{image_id}"
    damage_type = random.choice(list(DamageType))
    rarity = random.randint(1, 7)
    item_in = ItemCreateSchema(
        ingame_id=ingame_id,
        title_id=title_id,
        title=title,
        image_id=image_id,
        image_url=image_url,
        damage_type=damage_type,
        rarity=rarity,
    )
    return await crud.create_item(db, item_in)
