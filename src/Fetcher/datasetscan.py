import pandas as pd
from sqlalchemy.orm import Session
from ORMSchema import Base, Pokemon, Habitat, GrowthRate, Ability, Form, Move, Type, engine
from sqlalchemy import select

csv_path = "../../dataset/pokemon_dataset.csv"

df_pokemon = pd.read_csv(csv_path)

def load_data_to_db():
    with Session(engine) as session:
        for _, row in df_pokemon.iterrows():
            # Crear el objeto Pokémon principal
            pokemon = Pokemon(
                id=row['id'],
                name=row['name'],
                base_experience=row['base_experience'],
                height=row['height'],
                weight=row['weight'],
                is_default=row['is_default'],
                order=row['order'],
                growth_rate = GrowthRate(row['growth_rate']),
                is_legendary=row['is_legendary'],
                is_mythical=row['is_mythical'],
                gender_rate=row['gender_rate'],
                capture_rate=row['capture_rate'],
                base_happiness = row['base_happiness'] if pd.notna(row['base_happiness']) else None,
                held_items=row['held_items'],
                hp=row['hp'],
                attack=row['attack'],
                defense=row['defense'],
                special_attack=row['special-attack'],
                special_defense=row['special-defense'],
                speed=row['speed'],
                evolution=row['name_evolutions'] if pd.notna(row['name_evolutions']) else None,
                evolution_level=row['level_evolutions'] if pd.notna(row['level_evolutions']) else None
            )
            
            # Relacionar los habitats
            if pd.notna(row['habitat']):
                habitats = row['habitat'].split(",")  # Asume que los habitats están separados por comas
                for habitat in habitats:
                    pokemon.habitat.append(Habitat(habitat=habitat.strip()))
            

            # Relacionar las habilidades
            if pd.notna(row['abilities']):
                abilities = row['abilities'].split(",")  # Asume que las habilidades están separadas por comas
                for ability in abilities:
                    ability_name = ability.strip()
                    # Verificar si ya existe la relación
                    if ability_name not in {a.ability for a in pokemon.abilities}:
                        pokemon.abilities.append(Ability(ability=ability_name))


            # Relacionar las formas
            if pd.notna(row['forms']):
                forms = row['forms'].split(",")  # Asume que las formas están separadas por comas
                for form in forms:
                    pokemon.forms.append(Form(form=form.strip()))

            # Relacionar los movimientos
            if pd.notna(row['moves']):
                moves = row['moves'].split(",")  # Asume que los movimientos están separados por comas
                for move in moves:
                    pokemon.moves.append(Move(move=move.strip()))

            # Relacionar los tipos
            if pd.notna(row['types']):
                types = row['types'].split(",")  # Asume que los tipos están separados por comas
                for type_ in types:
                    pokemon.types.append(Type(type=type_.strip()))

            # Añadir el Pokémon a la sesión
            session.add(pokemon)
        
        # Confirmar los cambios en la base de datos
        session.commit()
        print("Datos cargados con éxito en la base de datos.")


if __name__ == "__main__":
    with Session(engine) as session:
        stmt = select(Pokemon)
        n = session.scalar(stmt)
        if n == None:
            load_data_to_db()