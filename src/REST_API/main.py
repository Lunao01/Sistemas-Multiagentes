
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

# get two random pokemons but only get ids, names and heights
@app.get("/search_pokemon/height")
def get_random_two_pokemons_height():
    with Session(engine) as session:
        # Select only id, name, and height of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.height).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "height": i[2]} for i in session.execute(stmt)]
        return pokemons

# get two random pokemons but only get ids, names and weights
@app.get("/search_pokemon/weight")
def get_random_two_pokemons_weight():
    with Session(engine) as session:
        # Select only id, name, and weight of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.weight).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "weight": i[2]} for i in session.execute(stmt)]
        return pokemons

# get two random pokemons where one is legendary and the other is not
@app.get("/search_pokemon/legendary")
def get_random_legendary_pokemon_and_not():
    with Session(engine) as session:
        # Select one legendary Pokémon and one non-legendary Pokémon
        legendary_stmt = select(Pokemon.id, Pokemon.name, Pokemon.is_legendary).where(Pokemon.is_legendary == True).order_by(func.random()).limit(1)
        non_legendary_stmt = select(Pokemon.id, Pokemon.name, Pokemon.is_legendary).where(Pokemon.is_legendary == False).order_by(func.random()).limit(1)
        
        legendary_pokemon = session.execute(legendary_stmt).first()
        non_legendary_pokemon = session.execute(non_legendary_stmt).first()
        
        # Return the results as a list of dictionaries
        pokemons = [
            {"id": legendary_pokemon[0], "name": legendary_pokemon[1], "is_legendary": legendary_pokemon[2]},
            {"id": non_legendary_pokemon[0], "name": non_legendary_pokemon[1], "is_legendary": non_legendary_pokemon[2]}
        ]
        
        return pokemons
    
# get two random pokemons where one is mythical and the other is not
@app.get("/search_pokemon/is_mythical")
def get_random_mythical_pokemon_and_not():
    with Session(engine) as session:
        # Select one mythical Pokémon and one non-mythical Pokémon
        mythical_stmt = select(Pokemon.id, Pokemon.name, Pokemon.is_mythical).where(Pokemon.is_mythical == True).order_by(func.random()).limit(1)
        non_mythical_stmt = select(Pokemon.id, Pokemon.name, Pokemon.is_mythical).where(Pokemon.is_mythical == False).order_by(func.random()).limit(1)
        
        mythical_pokemon = session.execute(mythical_stmt).first()
        non_mythical_pokemon = session.execute(non_mythical_stmt).first()
        
        # Return the results as a list of dictionaries
        pokemons = [
            {"id": mythical_pokemon[0], "name": mythical_pokemon[1], "is_mythical": mythical_pokemon[2]},
            {"id": non_mythical_pokemon[0], "name": non_mythical_pokemon[1], "is_mythical": non_mythical_pokemon[2]}
        ]
        
        return pokemons

# get two random pokemons but only get ids, names and hp
@app.get("/search_pokemon/hp")
def get_random_two_pokemons_hp():
    with Session(engine) as session:
        # Select only id, name, and weight of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.hp).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "hp": i[2]} for i in session.execute(stmt)]
        return pokemons
    
# get two random pokemons but only get ids, names and attacks
@app.get("/search_pokemon/attack")
def get_random_two_pokemons_attack():
    with Session(engine) as session:
        # Select only id, name, and attack of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.attack).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "attack": i[2]} for i in session.execute(stmt)]
        return pokemons

# get two random pokemons but only get ids, names and defenses
@app.get("/search_pokemon/defense")
def get_random_two_pokemons_defense():
    with Session(engine) as session:
        # Select only id, name, and defense of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.defense).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "defense": i[2]} for i in session.execute(stmt)]
        return pokemons

# get two random pokemons but only get ids, names and special attacks
@app.get("/search_pokemon/special-attack")
def get_random_two_pokemons_special_attack():
    with Session(engine) as session:
        # Select only id, name, and special attack of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.special_attack).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "special_attack": i[2]} for i in session.execute(stmt)]
        return pokemons
    
# get two random pokemons but only get ids, names and special defenses
@app.get("/search_pokemon/special-defense")
def get_random_two_pokemons_special_defense():
    with Session(engine) as session:
        # Select only id, name, and special defense of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.special_defense).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "special_defense": i[2]} for i in session.execute(stmt)]
        return pokemons

# get two random pokemons but only get ids, names and speeds
@app.get("/search_pokemon/speed")
def get_random_two_pokemons_speed():
    with Session(engine) as session:
        # Select only id, name, and speed of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.speed).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "speed": i[2]} for i in session.execute(stmt)]
        return pokemons

# get two random pokemons but only get ids, names and caputre rates
@app.get("/search_pokemon/capture_rate")
def get_random_two_pokemons_capture_rate():
    with Session(engine) as session:
        # Select only id, name, and capture rate of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.capture_rate).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "capture_rate": i[2]} for i in session.execute(stmt)]
        return pokemons

# get two random pokemons but only get ids, names and type
@app.get("/search_pokemon/types")
def get_random_two_pokemons_type():
    with Session(engine) as session:
        # Selecciona 2 Pokémon aleatorios y muestra todos sus tipos
        stmt = (
            select(Pokemon.id, Pokemon.name, func.array_agg(Type.type))
            .join(Type, Pokemon.id == Type.pokemon)
            .group_by(Pokemon.id, Pokemon.name)  # Agrupar por id y nombre del Pokémon
            .order_by(func.random())
            .limit(2)
        )
        pokemons = [{"id": id, "name": name, "type": types} for id, name, types in session.execute(stmt).all()]
        return pokemons
    

# get two random pokemons but only get ids, names and abilities
@app.get("/search_pokemon/abilities")
def get_random_two_pokemons_ability():
    with Session(engine) as session:
        # Selecciona 2 Pokémon aleatorios y muestra todos sus abilidades
        stmt = stmt = (
            select(Pokemon.id, Pokemon.name, func.array_agg(Ability.ability))
            .select_from(Pokemon)  # Explicitly state that Pokemon is the base table
            .join(Ability, Ability.pokemon == Pokemon.id)  # Join Pokemon with Ability
            .group_by(Pokemon.id, Pokemon.name)  # Group by id and name to allow aggregation
            .order_by(func.random())  # Order randomly
            .limit(2)  # Limit to 2 pokemons
        )

        pokemons = [{"id": id, "name": name, "abilities": abilities} for id, name, abilities in session.execute(stmt).all()]
        return pokemons

