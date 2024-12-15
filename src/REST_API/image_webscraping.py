# Librerías
import requests
from bs4 import BeautifulSoup
from io import BytesIO

def get_pokemon_img(pk):
    url = f"https://www.wikidex.net/wiki/{pk}"
    request = requests.get(url)
    soup = BeautifulSoup(request.content, 'html.parser')
    img = soup.find("div", class_ = "imagen imageswitch_section imageswitch_image imageswitch_scale")
    img_tag = img.find("a", class_ = "image").img
    
    if img_tag and 'srcset' in img_tag.attrs:
        # Divide el contenido de srcset y busca la URL de 400px
        srcset = img_tag['srcset'].split(", ")
        for url_size in srcset:
            if "400px" in url_size:
                img_url_400px = url_size.split(" ")[0]  # Extrae solo la URL sin el descriptor de tamaño
                return (img_url_400px, f"{pk}.png")

