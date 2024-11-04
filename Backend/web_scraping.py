# Librerías
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def main():
    # Pedir al usuario que ingrese un string
    pk = input("Por favor, ingresa un texto:")

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
                descargar_imagen(img_url_400px, f"{pk}.png")
                
   
def descargar_imagen(url, nombre_archivo):
    # Realiza la solicitud GET para descargar la imagen
    response = requests.get(url)
    
    # Verifica que la solicitud fue exitosa
    if response.status_code == 200:
        # Guarda el contenido en un archivo de imagen
        with open(nombre_archivo, 'wb') as file:
            file.write(response.content)
        print(f"Imagen guardada como {nombre_archivo}")
    else:
        print("Error al descargar la imagen.")


if __name__ == "__main__":
    main()
