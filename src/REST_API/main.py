
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from ORMSchema import Base, Pokemon, Habitat, GrowthRate, Ability, Form, Move, Type, engine
from pokemon import PokemonResponse
from sqlalchemy import select, func

# Inicializar la app
app = FastAPI()


# get pokemon by id
@app.get("/pokemon/{id}")
def get_pokemon_by_id(id: int):
  with Session(engine) as session:
    stmt = select(Pokemon).where(Pokemon.id == id)
    p = session.scalar(stmt)
    return PokemonResponse(p)
  
@app.get("/search_pokemon/random_two")
def get_random_two_pokemons():
  with Session(engine) as session:
    # Select two random Pokémon
    stmt = select(Pokemon).order_by(func.random()).limit(2)
    pokemons = [PokemonResponse(i) for i in session.scalars(stmt)]
    return pokemons
# get pokemon by 



