from ._orm_pokemon import Base, Pokemon, PokemonResponse, Habitat, GrowthRate, Ability, Form, Move, Type
from ._engine import engine
from ._orm_users import User, Cookie
Base.metadata.create_all(engine)
