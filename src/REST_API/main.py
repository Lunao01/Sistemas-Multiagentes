
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse
from httpx import HTTPTransport
from sqlalchemy.orm import Session
from ORMSchema import Base, Pokemon, Habitat, GrowthRate, Ability, Form, Move, Type, Score, User, engine
from pokemon import PokemonResponse
from sqlalchemy import select, func, desc
from random import sample
import requests
import image_webscraping
import os


# CONSTANTS 

MISSING_ITEMS_ERR = "Not enough items in pokemon database"
TYPE_404_ERR = "Type given doesn't exist"
POKEMON_404_ERR = "Pokemon not found"
ABILITY_404_ERR = "ability not found"
RANKING_404_ERR = "Error in ranking"

# Inicializar la app
app = FastAPI()


# get pokemon by id
@app.get("/pokemon/{id}")
def get_pokemon_by_id(id: int):
    with Session(engine) as session:
        stmt = select(Pokemon).where(Pokemon.id == id)
        p = session.scalar(stmt)
        if p == None:
            raise HTTPException(status_code=404, detail=POKEMON_404_ERR)
        return PokemonResponse(p)

# Get pokemon image by id
# @app.get("/pokemon_img/{id}")
  
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
@app.get("/search_pokemon/is_legendary")
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
            {"id": legendary_pokemon[0], "name": legendary_pokemon[1], "legendary": legendary_pokemon[2]},
            {"id": non_legendary_pokemon[0], "name": non_legendary_pokemon[1], "legendary": non_legendary_pokemon[2]}
        ]
        pokemons = sample(pokemons,2)
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
        pokemons = sample(pokemons, 2)
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
@app.get("/search_pokemon/special_attack")
def get_random_two_pokemons_special_attack():
    with Session(engine) as session:
        # Select only id, name, and special attack of two random Pokémon
        stmt = select(Pokemon.id, Pokemon.name, Pokemon.special_attack).order_by(func.random()).limit(2)
        pokemons = [{"id": i[0], "name": i[1], "special_attack": i[2]} for i in session.execute(stmt)]
        if len(pokemons) < 2:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        return pokemons
    
# get two random pokemons but only get ids, names and special defenses
@app.get("/search_pokemon/special_defense")
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
@app.get("/search_pokemon/types/{type}")
def get_random_two_pokemons_type(type:str):
    with Session(engine) as session:
        # Selecciona 2 Pokémon aleatorios y muestra todos sus tipos
        all_pokemon_with_type = (
            select(Pokemon.id)
            .join(Type, Type.pokemon == Pokemon.id)
            .where(Type.type == type)
        )
        stmt_t = (
            select(Pokemon.id, Pokemon.name, func.array_agg(Type.type))
            .join(Type, Pokemon.id == Type.pokemon)
            .where( Pokemon.id.in_(all_pokemon_with_type))
            .group_by(Pokemon.id, Pokemon.name)  # Agrupar por id y nombre del Pokémon
            .order_by(func.random())
            .limit(1)
        )
        stmt_nt = (
            select(Pokemon.id, Pokemon.name, func.array_agg(Type.type))
            .join(Type, Pokemon.id == Type.pokemon)
            .where( Pokemon.id.not_in(all_pokemon_with_type))
            .group_by(Pokemon.id, Pokemon.name)
            .order_by(func.random())
            .limit(1)
        )
        
        p0 = session.execute(stmt_t).first()
        p1 = session.execute(stmt_nt).first()

        types = [i.tuple()[0] for i in session.execute(select(Type.type).distinct()).all()]
        if (p0 == None or p1 == None) and len(types)==0:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        elif (p0 == None or p1 == None) and len(types) > 0:
            raise  HTTPException(status_code=404, detail=TYPE_404_ERR)
        
        pokemons = [p0.tuple(), p1.tuple()]
        pokemons = sample(pokemons,2)
        pokemons = [{'id':i[0],'name':i[1],'types':i[2]} for i in pokemons]
        return pokemons
    

# get two random pokemons but only get ids, names and abilities
@app.get("/search_pokemon/abilities/{ability}")
def get_random_two_pokemons_ability(ability:str):
    with Session(engine) as session:
        # Selecciona 2 Pokémon aleatorios y muestra todos sus abilidades
        all_pokemon_with_ability = (
            select(Pokemon.id)
            .join(Ability, Ability.pokemon == Pokemon.id)
            .where(Ability.ability == ability)
        )
        stmt_a = (
            select(Pokemon.id, Pokemon.name, func.array_agg(Ability.ability))
            .select_from(Pokemon)  # Explicitly state that Pokemon is the base table
            .join(Ability, Ability.pokemon == Pokemon.id)  # Join Pokemon with Ability
            .where(Pokemon.id.in_(all_pokemon_with_ability)) # Only select pokemon rows with the ability
            .group_by(Pokemon.id, Pokemon.name)  # Group by id and name to allow aggregation
            .order_by(func.random())  # Order randomly
            .limit(2)  # Limit to 2 pokemons
        )
        stmt_na = (
            select(Pokemon.id, Pokemon.name, func.array_agg(Ability.ability))
            .select_from(Pokemon)  # Explicitly state that Pokemon is the base table
            .join(Ability, Ability.pokemon == Pokemon.id)  # Join Pokemon with Ability
            .where( Pokemon.id.not_in(all_pokemon_with_ability)) # Only select pokemon rows with the ability
            .group_by(Pokemon.id, Pokemon.name)  # Group by id and name to allow aggregation
            .order_by(func.random())  # Order randomly
            .limit(2)  # Limit to 2 pokemons
        )

        p0 = session.execute(stmt_a).first()
        p1 = session.execute(stmt_na).first()

        abilities = [i.tuple()[0] for i in session.execute(select(Ability.ability).distinct()).all()]
        if (p0 == None or p1 == None) and len(abilities)==0:
            raise HTTPException(status_code=500, detail=MISSING_ITEMS_ERR)
        elif (p0 == None or p1 == None) and len(abilities) > 0:
            raise  HTTPException(status_code=404, detail=TYPE_404_ERR)
        
        pokemons = [p0.tuple(), p1.tuple()]
        pokemons = sample(pokemons,2)
        pokemons = [{'id':i[0],'name':i[1],'abilities':i[2]} for i in pokemons]
        return pokemons

@app.get("/search_misc/random/types")
def get_random_type():
    with Session(engine) as session:
        stmt = select(Type.type).distinct()
        t = sample(session.execute(stmt).all(),1)
        if t == None:
            raise HTTPException(status_code=500, detail=TYPE_404_ERR)
        return t[0][0]

@app.get("/search_misc/random/abilities")
def get_random_ability():
    with Session(engine) as session:
        stmt = select(Ability.ability).distinct()
        a = sample(session.execute(stmt).all(),1)
        if a == None:
            raise HTTPException(status_code=500, detail=ABILITY_404_ERR)
        return a[0][0]

    

# Endpoint para obtener la imagen de un Pokémon
@app.get("/pokemon_img/{id}")
def get_pokemon_img_endpoint(id: str):
    # Obtener la URL y el nombre de archivo de la imagen usando la función de image_webscraping2
    url, filename = image_webscraping.get_pokemon_img(id)
    
    # Verificar si se obtuvo una imagen válida
    if url:
        save_directory = "/img"
        
        # Construir la ruta completa para guardar la imagen
        file_path = os.path.join(save_directory, filename)

        # Comprobar si la imagen ya existe
        if os.path.exists(file_path):
            # Si la imagen ya está descargada, no la descargamos nuevamente
            return FileResponse(file_path)
        
        # Descargar la imagen
        response = requests.get(url)

        # Verificar que la solicitud fue exitosa
        if response.status_code == 200:
            # Guardar la imagen en el archivo
            with open(file_path, 'wb') as file:
                file.write(response.content)

            # Retornar la imagen guardada como respuesta
            return FileResponse(file_path)
        else:
            return {"error": "Failed to download the image."}
    else:
        return {"error": "Image not found for this Pokémon ID."}

# Endpoint para obtener el top 10 de usuarios con el ranking más alto
@app.get("/users/top/{n}")
def get_top_10_users(n : int):
    with Session(engine) as session:
        # Obtener los usuarios con los puntajes más altos, ordenados de mayor a menor
        stmt = (
            select(User.username, Score.score)
            .join(Score, User.id == Score.user_id)
            .order_by(desc(Score.score))
            .limit(n)
        )
        top_users = session.execute(stmt).fetchall()

        # Si no hay resultados, devolver error
        if not top_users:
            raise HTTPException(status_code=404, detail=RANKING_404_ERR)

        # Formatear los resultados en un formato amigable
        return [
            {"username": user.username, "score": user.score}
            for user in top_users
        ]