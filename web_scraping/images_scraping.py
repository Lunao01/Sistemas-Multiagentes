# - The webscraping is carried out from PokéAPI:
#     - Link: https://pokeapi.co/

# - You can check the PokéAPI docs section to search all possible trackeable information about pokémons. 
# - The pokémon data has JSON format.
#     - PokéAPI docs section: https://pokeapi.co/docs/v2

# You can check the documentation part that explains PokemonSprites - front_default.
# Hence, you can see the explanation of the front_default attribute. Recommended: Use CTRL + F to search for the front_default attribute.
#     - Exapmle to scrap: front_default:"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/35.png"

import requests
import os

# Directory to save the Pokémon images
image_dir = 'pokemon_images'
os.makedirs(image_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Base URL of the PokéAPI for Pokémon data
base_url = 'https://pokeapi.co/api/v2/pokemon/'

def download_pokemon_image(pokemon_id):
    """Downloads the front image for a Pokémon if available."""
    # Construct the URL for the Pokémon data
    url = f'{base_url}{pokemon_id}'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve data for Pokémon ID {pokemon_id}")
        return
    
    # Parse the JSON data
    data = response.json()
    front_default_url = data['sprites'].get('front_default')
    
    # Check if an image is available and download it
    if front_default_url:
        image_path = os.path.join(image_dir, f"{pokemon_id}.png")
        image_response = requests.get(front_default_url)
        
        if image_response.status_code == 200:
            with open(image_path, 'wb') as img_file:
                img_file.write(image_response.content)
            print(f"Image saved for Pokémon ID {pokemon_id}")
        else:
            print(f"Failed to download image for Pokémon ID {pokemon_id}")
    else:
        print(f"No image available for Pokémon ID {pokemon_id}")

# Range of Pokémon IDs to scrape images for
start_id = 1020
end_id = 1025

# Loop through specified range and download images
for pokemon_id in range(start_id, end_id + 1):
    print(f"Attempting to download image for Pokémon ID {pokemon_id}...")
    download_pokemon_image(pokemon_id)

print("Image scraping completed.")
