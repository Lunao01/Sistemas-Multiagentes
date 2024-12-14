from typing import List
import enum
from sqlalchemy import Enum, Integer, Boolean, ForeignKey, UnicodeText
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column


class GrowthRate(enum.Enum):
    slow = 1
    medium_slow = 2
    medium = 3
    fast = 4
    slow_then_very_fast = 5


class Base(DeclarativeBase):
    pass


class Pokemon(Base):
    __tablename__ = "pokemon"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(UnicodeText())
    base_experience: Mapped[int] = mapped_column(Integer())
    height: Mapped[int] = mapped_column(Integer())
    weight: Mapped[int] = mapped_column(Integer())
    is_default: Mapped[bool] = mapped_column(Boolean())
    order: Mapped[int] = mapped_column(Integer())
    habitat: Mapped[List["Habitat"]] = relationship(cascade="all, delete-orphan")
    growth_rate: Mapped[GrowthRate] = mapped_column(Enum(GrowthRate))
    is_legendary: Mapped[bool] = mapped_column(Boolean())
    is_mythical: Mapped[bool] = mapped_column(Boolean())
    gender_rate: Mapped[int] = mapped_column(Integer())

    capture_rate: Mapped[int] = mapped_column(Integer())
    base_happiness: Mapped[int] = mapped_column(Integer())
    abilities: Mapped[List["Ability"]] = relationship(cascade="all, delete-orphan")
    forms: Mapped[List["Form"]] = relationship(cascade="all, delete-orphan")
    held_items: Mapped[bool] = mapped_column(Boolean())
    moves: Mapped[List["Move"]] = relationship(cascade="all, delete-orphan")
    types: Mapped[List["Type"]] = relationship(cascade="all, delete-orphan")
    hp: Mapped[int] = mapped_column(Integer())
    attack: Mapped[int] = mapped_column(Integer())
    defense: Mapped[int] = mapped_column(Integer())
    special_attack: Mapped[int] = mapped_column(Integer())
    special_defense: Mapped[int] = mapped_column(Integer())
    speed: Mapped[int] = mapped_column(Integer())
    evolution: Mapped[str] = mapped_column(UnicodeText(),nullable=True)
    evolution_level: Mapped[int] = mapped_column(Integer(),nullable=True)


class Habitat(Base):
    __tablename__ = "habitat"
    habitat: Mapped[str] = mapped_column(UnicodeText(), primary_key=True)
    pokemon: Mapped[int] = mapped_column(
        Integer(), ForeignKey("pokemon.id"), primary_key=True
    )


class Ability(Base):
    __tablename__ = "ability"
    ability: Mapped[str] = mapped_column(UnicodeText(), primary_key=True)
    pokemon: Mapped[int] = mapped_column(
        Integer(), ForeignKey("pokemon.id"), primary_key=True
    )


class Form(Base):
    __tablename__ = "form"
    form: Mapped[str] = mapped_column(UnicodeText(), primary_key=True)
    pokemon: Mapped[int] = mapped_column(
        Integer(), ForeignKey("pokemon.id"), primary_key=True
    )


class Move(Base):
    __tablename__ = "move"
    move: Mapped[str] = mapped_column(UnicodeText(), primary_key=True)
    pokemon: Mapped[int] = mapped_column(
        Integer(), ForeignKey("pokemon.id"), primary_key=True
    )


class Type(Base):
    __tablename__ = "type"
    type: Mapped[str] = mapped_column(UnicodeText(), primary_key=True)
    pokemon: Mapped[int] = mapped_column(
        Integer(), ForeignKey("pokemon.id"), primary_key=True
    )
