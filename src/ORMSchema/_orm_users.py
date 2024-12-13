from typing import Any, List
from sqlalchemy import Column, ForeignKey, String, Table, UnicodeText, Integer
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
    user: Mapped[int] = mapped_column(
        Integer(), ForeignKey("users.id"), primary_key=True
    )
    score: Mapped[int] = mapped_column(Integer())


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(UnicodeText, unique=True)
    password_hash: Mapped[bytes] = mapped_column(
        String(64)
    )  # 64 bytes 512 bits, for sha512, the hash algorithm used