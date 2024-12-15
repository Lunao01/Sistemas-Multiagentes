
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from ORMSchema import Base, Pokemon, Habitat, GrowthRate, Ability, Form, Move, Type, engine
from pokemon import PokemonResponse
from sqlalchemy import select, func
from random import sample


# CONSTANTS 

MISSING_ITEMS_ERR = "Not enough items in pokemon database"


# Inicializar la app
app = FastAPI()


# get pokemon by id
@app.get("/pokemon/{id}")
def get_pokemon_by_id(id: int):
    with Session(engine) as session:
        stmt = select(Pokemon).where(Pokemon.id == id)
        p = session.scalar(stmt)
        if p == None:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return PokemonResponse(p)
  
@app.get("/search_pokemon/random_two")
def get_random_two_pokemons():
    with Session(engine) as session:
        # Select two random Pokémon
        stmt = select(Pokemon).order_by(func.random()).limit(2)
        pokemons = [PokemonResponse(i) for i in session.scalars(stmt)]
        if len(pokemons)<2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons

# get two random pokemons but only get ids, names and heights
@app.get("/search_pokemon/height")
def get_random_two_pokemons_height():
    with Session(engine) as session:
        # Select only id, name, and height of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.height).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "height": i[2]} for i in session.execute(stmt)]
        if len(pokemons)<2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons

# get two random pokemons but only get ids, names and weights
@app.get("/search_pokemon/weight")
def get_random_two_pokemons_weight():
    with Session(engine) as session:
        # Select only id, name, and weight of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.weight).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "weight": i[2]} for i in session.execute(stmt)]
        if len(pokemons)<2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
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
        
        if legendary_pokemon == None or non_legendary_pokemon == None:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        
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
        
        if mythical_pokemon == None or non_mythical_pokemon == None:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)

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
        if len(pokemons) < 2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons
    
# get two random pokemons but only get ids, names and attacks
@app.get("/search_pokemon/attack")
def get_random_two_pokemons_attack():
    with Session(engine) as session:
        # Select only id, name, and attack of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.attack).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "attack": i[2]} for i in session.execute(stmt)]
        if len(pokemons) < 2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons

# get two random pokemons but only get ids, names and defenses
@app.get("/search_pokemon/defense")
def get_random_two_pokemons_defense():
    with Session(engine) as session:
        # Select only id, name, and defense of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.defense).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "defense": i[2]} for i in session.execute(stmt)]
        if len(pokemons) < 2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons

# get two random pokemons but only get ids, names and special attacks
@app.get("/search_pokemon/special-attack")
def get_random_two_pokemons_special_attack():
    with Session(engine) as session:
        # Select only id, name, and special attack of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.special_attack).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "special_attack": i[2]} for i in session.execute(stmt)]
        if len(pokemons) < 2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons
    
# get two random pokemons but only get ids, names and special defenses
@app.get("/search_pokemon/special-defense")
def get_random_two_pokemons_special_defense():
    with Session(engine) as session:
        # Select only id, name, and special defense of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.special_defense).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "special_defense": i[2]} for i in session.execute(stmt)]
        if len(pokemons) < 2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons

# get two random pokemons but only get ids, names and speeds
@app.get("/search_pokemon/speed")
def get_random_two_pokemons_speed():
    with Session(engine) as session:
        # Select only id, name, and speed of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.speed).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "speed": i[2]} for i in session.execute(stmt)]
        if len(pokemons) < 2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons

# get two random pokemons but only get ids, names and caputre rates
@app.get("/search_pokemon/capture_rate")
def get_random_two_pokemons_capture_rate():
    with Session(engine) as session:
        # Select only id, name, and capture rate of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.capture_rate).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "capture_rate": i[2]} for i in session.execute(stmt)]
        if len(pokemons) < 2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons

# get two random pokemons but only get ids, names and type. At least 1 pokemon will have the type {type}
@app.get("/search_pokemon/types")
def get_random_two_pokemons_type():
    type = 'water'
    try:
        with Session(engine) as session:
            # Selecciona 2 Pokémon aleatorios y muestra todos sus tipos
            stmt_t = (
                select(Pokemon.id, Pokemon.name, func.array_agg(Type.type))
                .join(Type, Pokemon.id == Type.pokemon)
                .where( Type.type == type)
                .group_by(Pokemon.id, Pokemon.name)  # Agrupar por id y nombre del Pokémon
                .order_by(func.random())
                .limit(1)
            )
            stmt_nt = (
                select(Pokemon.id, Pokemon.name, func.array_agg(Type.type))
                .join(Type, Pokemon.id == Type.pokemon)
                .where( Type.type != type)
                .group_by(Pokemon.id, Pokemon.name)
                .order_by(func.random())
                .limit(1)
            )
            p0 = session.execute(stmt_t).first()
            p1 = session.execute(stmt_nt).first()
            if p0 == None or p1 == None:
                raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
            pokemons = [p0.tuple(), p1.tuple()]
            pokemons = sample(pokemons,2)
            return pokemons
    except Exception as e:
        print(e)
    

# get two random pokemons but only get ids, names and abilities
@app.get("/search_pokemon/abilities/{ability}")
def get_random_two_pokemons_ability(ability:str):
    with Session(engine) as session:
        # Selecciona 2 Pokémon aleatorios y muestra todos sus abilidades
        stmt_a = (
            select(Pokemon.id, Pokemon.name, func.array_agg(Ability.ability))
            .select_from(Pokemon)  # Explicitly state that Pokemon is the base table
            .join(Ability, Ability.pokemon == Pokemon.id)  # Join Pokemon with Ability
            .where( Type.type == type)
            .group_by(Pokemon.id, Pokemon.name)  # Group by id and name to allow aggregation
            .order_by(func.random())  # Order randomly
            .limit(2)  # Limit to 2 pokemons
        )
        stmt_na = (
            select(Pokemon.id, Pokemon.name, func.array_agg(Ability.ability))
            .select_from(Pokemon)  # Explicitly state that Pokemon is the base table
            .join(Ability, Ability.pokemon == Pokemon.id)  # Join Pokemon with Ability
            .where( Type.type != type)
            .group_by(Pokemon.id, Pokemon.name)  # Group by id and name to allow aggregation
            .order_by(func.random())  # Order randomly
            .limit(2)  # Limit to 2 pokemons
        )

        pokemons = [session.execute(stmt_a).first(), session.execute(stmt_na).first()]
        if None in pokemons:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons

@app.get("/search_misc/types")
def get_random_type():
    with Session(engine) as session:
        select(Type.type).distinct()