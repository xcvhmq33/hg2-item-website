import uuid

from hg2_item_parser.enums import DamageType, WeaponType
from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class PropertiesBaseSchema(BaseModel):
    max_lvl: int = Field(ge=1, le=99)
    cost: int | None = Field(default=None, ge=0)
    max_lvl_damage: int | None = Field(default=None, ge=0)
    max_lvl_ammo: int | None = Field(default=None, ge=-1)
    max_lvl_atk_speed: float | None = Field(default=None, ge=0)
    max_lvl_hp: int | None = Field(default=None, ge=0)
    weapon_type: WeaponType | None = None
    deploy_limit: int | None = Field(default=None, ge=0)
    duration: float | None = Field(default=None, ge=0)
    crit_rate: float | None = Field(default=None, ge=0)
    base_sync: int | None = Field(default=None, ge=0)
    max_sync: int | None = Field(default=None, ge=0)
    item_id: int = Field(ge=1)


class SkillBaseSchema(BaseModel):
    ingame_id: int = Field(ge=1)
    title_id: int = Field(ge=0)
    title: str = Field(min_length=1, max_length=64)
    description_template_id: int = Field(ge=0)
    description_template: str = Field(min_length=1)
    description: str = Field(min_length=1)
    damage_type: DamageType | None = None
    item_id: int = Field(ge=1)


class ItemBaseSchema(BaseModel):
    ingame_id: int = Field(ge=1)
    title_id: int = Field(ge=0)
    title: str = Field(max_length=64)
    image_id: int = Field(ge=0)
    image_url: HttpUrl
    damage_type: DamageType | None = None
    rarity: int = Field(ge=1, le=7)


class UserBaseSchema(BaseModel):
    email: EmailStr = Field(max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    name: str = Field(max_length=32)


class PropertiesReadSchema(PropertiesBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class SkillReadSchema(SkillBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ItemReadSchema(ItemBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int
    properties: PropertiesReadSchema | None
    skills: list[SkillReadSchema]


class UserReadSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID


class PropertiesCreateSchema(PropertiesBaseSchema): ...


class SkillCreateSchema(SkillBaseSchema): ...


class ItemCreateSchema(ItemBaseSchema): ...


class UserCreateSchema(UserBaseSchema):
    password: str = Field(min_length=8, max_length=40)


class UserLoginSchema(BaseModel):
    name: str = Field(max_length=32)
    password: str


class UserRegisterSchema(UserLoginSchema):
    email: EmailStr = Field(max_length=255)
