# Librerías
import json
import random
import os

file_path = 'static/json/questions.json'

# Método para cargar el archivo JSON y obtener una pregunta aleatoria
def generate_question() -> dict[str,str]:
    # Abre y carga el archivo JSON
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Selecciona una pregunta aleatoria
    question = random.choice(data['questions'])
    
    # Devuelve la pregunta y sus atributos
    return question