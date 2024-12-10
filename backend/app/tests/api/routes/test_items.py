import random

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.tests.utils.item import create_random_item


@pytest.mark.asyncio
async def test_read_item(client: AsyncClient, db: AsyncSession) -> None:
    item = await create_random_item(db)
    response = await client.get(
        f"{settings.API_V1_STR}/items/{item.ingame_id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["ingame_id"] == item.ingame_id
    assert content["title"] == item.title
    assert content["image_url"] == item.image_url
    assert content["damage_type"] == item.damage_type.value
    assert content["rarity"] == item.rarity
    assert content["id"] == item.id


@pytest.mark.asyncio
async def test_read_item_not_found(client: AsyncClient) -> None:
    response = await client.get(
        f"{settings.API_V1_STR}/items/{random.randint(6000, 99999)}",
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Item not found"


@pytest.mark.asyncio
async def test_read_items(client: AsyncClient, db: AsyncSession) -> None:
    await create_random_item(db)
    await create_random_item(db)
    response = await client.get(
        f"{settings.API_V1_STR}/items/",
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 2
