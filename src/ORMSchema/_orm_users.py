import base64
from typing import Any, List
from sqlalchemy import Column, ForeignKey, String, Table, UnicodeText, Integer, BINARY
from ._orm_pokemon import Base, Pokemon
from sqlalchemy.orm import Mapped, mapped_column, relationship

pokemon_unlocked_by = Table(
    "pokemon_unlocked_tbl",
    Base.metadata,
    Column("pokemon", ForeignKey("pokemon.id"), primary_key=True),
    Column("user", ForeignKey("users.id"), primary_key=True),
)


class Score(Base):
    __tablename__ = "scores"
    id: Mapped[int] = mapped_column(primary_key=True)
    score: Mapped[int] = mapped_column(Integer())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(UnicodeText, unique=True)
    password_hash: Mapped[str] = mapped_column(
        String(128) 
    )  # for sha512, the hash algorithm used
    cookies: Mapped[List["Cookie"]] = relationship(cascade="all, delete-orphan")
    scores: Mapped[List["Score"]] = relationship(cascade="all, delete-orphan")
    unlocked_pokemon: Mapped[List["Pokemon"]] = relationship(secondary=pokemon_unlocked_by)

class Cookie(Base):
    __tablename__ = "cookies"
    id: Mapped[str] = mapped_column(String(88), primary_key=True)
    user: Mapped[int] = mapped_column(Integer(), ForeignKey("users.id"))
