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
    item_ingame_id: int = Field(ge=1)


class SkillBaseSchema(BaseModel):
    ingame_id: int = Field(ge=1)
    title_id: int = Field(ge=0)
    title: str = Field(min_length=1, max_length=64)
    description_template_id: int = Field(ge=0)
    description_template: str = Field(min_length=1)
    description: str = Field(min_length=1)
    damage_type: DamageType | None = None
    item_ingame_id: int = Field(ge=1)


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
    name: str = Field(max_length=32)
    is_active: bool = True
    is_superuser: bool = False


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


class ItemsReadSchema(BaseModel):
    data: list[ItemReadSchema]
    count: int


class UserReadSchema(UserBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID


class UsersReadSchema(BaseModel):
    data: list[UserReadSchema]
    count: int


class PropertiesCreateSchema(PropertiesBaseSchema): ...


class SkillCreateSchema(SkillBaseSchema): ...


class ItemCreateSchema(ItemBaseSchema): ...


class UserCreateSchema(UserBaseSchema):
    password: str = Field(min_length=8, max_length=40)


class UserUpdateMeSchema(BaseModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    name: str | None = Field(default=None, max_length=32)


class UserUpdateSchema(UserUpdateMeSchema):
    password: str | None = Field(default=None, min_length=8, max_length=40)
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserLoginSchema(BaseModel):
    name: str = Field(max_length=32)
    password: str = Field(min_length=8, max_length=40)


class UserRegisterSchema(UserLoginSchema):
    email: EmailStr = Field(max_length=255)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None


class Message(BaseModel):
    message: str


class UpdatePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)
