from ._orm_pokemon import Base, Pokemon, Habitat, GrowthRate, Ability, Form, Move, Type
from ._engine import engine
from ._orm_users import User
Base.metadata.create_all(engine)
