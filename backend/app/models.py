import uuid

from hg2_item_parser.enums import DamageType, WeaponType
from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase, MappedAsDataclass, AsyncAttrs): ...


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    ingame_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    title_id: Mapped[int]
    title: Mapped[str] = mapped_column(String(64))
    image_id: Mapped[int]
    image_url: Mapped[str]
    damage_type: Mapped[DamageType] = mapped_column(nullable=True)
    rarity: Mapped[int]

    properties: Mapped["Properties"] = relationship(
        "Properties", back_populates="item", cascade="all, delete-orphan", init=False
    )
    skills: Mapped[list["Skill"]] = relationship(
        "Skill", back_populates="item", cascade="all, delete-orphan", init=False
    )


class Properties(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(primary_key=True)
    max_lvl: Mapped[int]
    cost: Mapped[int] = mapped_column(nullable=True)
    max_lvl_damage: Mapped[int] = mapped_column(nullable=True)
    max_lvl_ammo: Mapped[int] = mapped_column(nullable=True)
    max_lvl_atk_speed: Mapped[float] = mapped_column(nullable=True)
    max_lvl_hp: Mapped[int] = mapped_column(nullable=True)
    weapon_type: Mapped[WeaponType] = mapped_column(nullable=True)
    deploy_limit: Mapped[int] = mapped_column(nullable=True)
    duration: Mapped[float] = mapped_column(nullable=True)
    crit_rate: Mapped[float] = mapped_column(nullable=True)
    base_sync: Mapped[int] = mapped_column(nullable=True)
    max_sync: Mapped[int] = mapped_column(nullable=True)
    item_ingame_id: Mapped[int] = mapped_column(ForeignKey("item.ingame_id"))

    item: Mapped["Item"] = relationship("Item", back_populates="properties")


class Skill(Base):
    __tablename__ = "skill"

    id: Mapped[int] = mapped_column(primary_key=True)
    ingame_id: Mapped[int]
    title_id: Mapped[int]
    title: Mapped[str] = mapped_column(String(64))
    description_template_id: Mapped[int]
    description_template: Mapped[str]
    description: Mapped[str]
    damage_type: Mapped[DamageType] = mapped_column(nullable=True)
    item_ingame_id: Mapped[int] = mapped_column(ForeignKey("item.ingame_id"))

    item: Mapped["Item"] = relationship("Item", back_populates="skills")


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        default_factory=uuid.uuid4, primary_key=True, init=False
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
