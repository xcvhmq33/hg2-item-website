from __future__ import annotations

from hg2_item_parser.enums import DamageType, WeaponType
from pydantic import BaseModel


class ItemBaseSchema(BaseModel):
    ingame_id: int
    title: str
    image_url: str
    damage_type: DamageType | None
    rarity: int


class ItemCreateSchema(ItemBaseSchema):
    pass


class ItemReadSchema(ItemBaseSchema):
    id: int
    properties: PropertiesReadSchema | None
    skills: list[SkillReadSchema]

    class Config:
        orm_mode = True


class PropertiesBaseSchema(BaseModel):
    max_lvl: int
    cost: int | None
    max_lvl_damage: int | None
    max_lvl_ammo: int | None
    max_lvl_atk_speed: float | None
    max_lvl_hp: int | None
    weapon_type: WeaponType | None
    deploy_limit: int | None
    duration: float | None
    crit_rate: float | None
    base_sync: int | None
    max_sync: int | None


class PropertiesCreateSchema(PropertiesBaseSchema):
    item_id: int


class PropertiesReadSchema(PropertiesBaseSchema):
    id: int

    class Config:
        orm_mode = True


class SkillBaseSchema(BaseModel):
    ingame_id: int
    title: str
    description: str
    damage_type: DamageType | None


class SkillCreateSchema(SkillBaseSchema):
    item_id: int


class SkillReadSchema(SkillBaseSchema):
    id: int

    class Config:
        orm_mode = True
