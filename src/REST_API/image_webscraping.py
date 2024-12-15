# - The webscraping is carried out from PokéAPI:
#     - Link: https://pokeapi.co/

# - You can check the PokéAPI docs section to search all possible trackeable information about pokémons. 
# - The pokémon data has JSON format.
#     - PokéAPI docs section: https://pokeapi.co/docs/v2

# You can check the documentation part that explains PokemonSprites - front_default.
# Hence, you can see the explanation of the front_default attribute. Recommended: Use CTRL + F to search for the front_default attribute.
#     - Exapmle to scrap: front_default:"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/35.png"
import requests

def get_pokemon_img(pokemon_id):
    # La URL base de la PokéAPI para obtener información de Pokémon
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    
    # Realizar la solicitud GET a la API
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        data = response.json()
        
        # Extraemos la URL de la imagen del Pokémon (front_default)
        image_url = data['sprites']['other']['official-artwork']['front_default']  # Corrected to get the URL
        
        # Verificamos si existe una imagen
        if image_url:
            # Usar el ID del Pokémon como nombre del archivo de la imagen
            filename = f"{pokemon_id}.png"  # Nombre del archivo basado en el ID
            return image_url, filename
        else:
            print(f"No image found for Pokémon ID {pokemon_id}.")
            return None, None
    else:
        print(f"Error fetching Pokémon data: {response.status_code}")
        return None, None
