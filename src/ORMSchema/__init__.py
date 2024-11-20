from typing import List
import enum
from sqlalchemy import Enum, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column


class GrowthRate(enum.Enum):
    # TODO add the rest of the growth rates. 
    # There seems to be a lot in the dataset, we will need to scan them i think
    slow = 1
    medium = 2
    fast = 3

class Base(DeclarativeBase):
    pass

class Pokemon(Base):
    __tablename__ = "pokemon"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    base_experience: Mapped[int] = mapped_column(Integer())
    height: Mapped[int] = mapped_column(Integer())
    weight: Mapped[int]= mapped_column(Integer())
    is_default: Mapped[bool]= mapped_column(Boolean())
    order: Mapped[int]= mapped_column(Integer())
    habitat: Mapped[List["Habitat"]] = relationship(
        back_populates="pokemon", cascade="all, delete-orphan"
    )
    growth_rate: Mapped[GrowthRate] = mapped_column(Enum(GrowthRate))
    is_legendary: Mapped[bool] = mapped_column(Boolean())
    is_mythical: Mapped[bool] = mapped_column(Boolean())
    gender_rate: Mapped[int] = mapped_column(Integer())

    capture_rate: Mapped[int] = mapped_column(Integer())
    base_happiness: Mapped[int] = mapped_column(Integer())
    abilities: Mapped[List["Ability"]] = relationship(
        back_populates="pokemon", cascade="all, delete-orphan"
    )
    forms: Mapped[List["Form"]] = relationship(
        back_populates="pokemon", cascade="all, delete-orphan"
    )
    held_items: Mapped[Boolean] = mapped_column(Boolean())
    moves: Mapped[List["Move"]] = relationship(
        back_populates="pokemon", cascade="all, delete-orphan"
    )
    types: Mapped[List["Type"]] = relationship(
        back_populates="pokemon", cascade="all, delete-orphan"
    )
    hp: Mapped[int] = mapped_column(Integer())
    attack: Mapped[int] = mapped_column(Integer())
    defense: Mapped[int] = mapped_column(Integer())
    special_attack: Mapped[int] = mapped_column(Integer())
    special_defense: Mapped[int] = mapped_column(Integer())
    speed: Mapped[int] = mapped_column(Integer())

class Habitat(Base):
    __tablename__ = "habitat"
    id: Mapped[str] = mapped_column(String(30),primary_key=True)
    pokemon: Mapped[int] = mapped_column(Integer(), ForeignKey("pokemon.id"), primary_key=True)
    
class Ability(Base):
    __tablename__ = "ability"
    id: Mapped[str] = mapped_column(String(30),primary_key=True)
    pokemon: Mapped[int] = mapped_column(Integer(), ForeignKey("pokemon.id"), primary_key=True)

class Form(Base):
    __tablename__ = "form"
    id: Mapped[str] = mapped_column(String(75),primary_key=True)
    pokemon: Mapped[int] = mapped_column(Integer(), ForeignKey("pokemon.id"), primary_key=True)

class Move(Base):
    __tablename__ = "move"
    id: Mapped[str] = mapped_column(String(75),primary_key=True)
    pokemon: Mapped[int] = mapped_column(Integer(), ForeignKey("pokemon.id"), primary_key=True)

class Type(Base):
    __tablename__ = "type"
    id: Mapped[str] = mapped_column(String(30),primary_key=True)
    pokemon: Mapped[int] = mapped_column(Integer(), ForeignKey("pokemon.id"), primary_key=True)