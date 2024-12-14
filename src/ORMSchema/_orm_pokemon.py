from typing import List
import enum
from sqlalchemy import Enum, Integer, Boolean, ForeignKey, UnicodeText
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from pydantic import BaseModel


class GrowthRate(enum.Enum):
    slow = 1
    medium_slow = 2
    medium = 3
    fast = 4
    slow_then_very_fast = 5


class Base(DeclarativeBase):
    pass

class PokemonResponse(BaseModel):
    def __init__(self, p: "Pokemon"):
        self.id: int = p.id
        self.name: str = p.name
        self.base_experience: int = p.base_experience
        self.height: int = p.height
        self.weight: int = p.weight
        self.is_default: bool = p.is_default
        self.order: int = p.order
        self.habitat: List[str] = [i.habitat for i in p.habitat]
        self.growth_rate: GrowthRate = p.growth_rate
        self.is_legendary: bool = p.is_legendary
        self.is_mythical: bool = p.is_mythical
        self.gender_rate: int = p.gender_rate

        self.capture_rate: int = p.capture_rate
        self.base_happiness: int = p.base_happiness
        self.abilities: List[str] = [i.ability for i in p.abilities]
        self.forms: List[str] = [i.form for i in p.forms]
        self.held_items: bool = p.held_items
        self.moves: List[str] = [i.move for i in p.moves]
        self.types: List[str] = [i.type for i in p.types]
        self.hp: int = p.hp
        self.attack: int = p.attack
        self.defense: int = p.defense
        self.special_attack: int = p.special_attack
        self.special_defense: int = p.special_defense
        self.speed: int = p.speed
        self.evolution: str = p.evolution
        self.evolution_level: int = p.evolution_level


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
