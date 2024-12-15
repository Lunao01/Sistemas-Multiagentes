from typing import Any, Tuple
from flask import Flask, render_template, request, redirect, url_for
from config import config # archivo config.py
from ORMSchema import engine, User, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import select
import hashlib 
import base64
import os
import question_generator 
import requests

app = Flask(__name__)
SESSION = "session"
BASE_URL = "http://rest_api:8000/"
d_score:dict[int,Any] = dict() # Guardar el puntaje del usuario en la partida
GLOBAL_CONTEXT = {
    "base_url": BASE_URL,
}

# Nada más cargar la ruta raíz te reenvia a /login
@app.route('/')
def index():
    return redirect(url_for('login'))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username'] # username del formulario
        password = request.form['password'] # password del formulario

        # Se comprueba si el usuario existe y la contraseña es correcta
        with Session(engine) as session:
            stmt = select(User).where(User.username == user) # SELECT * FROM users WHERE username = 'user';
            db_user = session.scalar(stmt) 

            
        if db_user is None:
            # Si el usuario no existe en la base de datos
            # print("Usuario no encontrado.")
            return render_template('auth/login.html', message="User not found.",**GLOBAL_CONTEXT)
        
        else:
            # Verificar la contraseña usando el hash almacenado
            password_hash = hash_gen(password)
            if db_user.password_hash == password_hash:
                # print("Login exitoso.")
                cookie = base64.b64encode(os.urandom(66)).decode()

                with Session(engine) as session:
                    # Guardar cookie
                    db_user = session.scalar(stmt)
                    db_user.cookies.append(Cookie(id = cookie)) # session.scalar(stmt) = db_user
                    session.commit()

                # Asignamos la cookie a la sesión actual
                response = redirect(url_for('menu')) 
                response.set_cookie(SESSION, cookie)
                return response
            
            else:
                return render_template('auth/login.html', message="Incorrect password.",**GLOBAL_CONTEXT)

    else: # Si es GET se renderiza la página login.html
        return render_template('auth/login.html',**GLOBAL_CONTEXT) # ruta de la plantilla html index


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username'] # username del formulario
        password = request.form['password'] # password del formulario
        password_repeat = request.form['password_repeat'] # password del formulario

        if password == password_repeat:
            with Session(engine) as session:
                stmt = select(User).where(User.username == user) # SELECT * FROM users WHERE username = 'user';
                db_user = session.scalar(stmt) 

                
                if db_user is None:
                    # Si el usuario no existe en la base de datos crea el usuario
                    password_hash = hash_gen(password)
                    new_user = User(username = user, password_hash = password_hash)
                    session.add(new_user)
                    session.commit()
                    # print("Cuenta creada.")
                
                else:
                    return render_template('auth/register.html', message="The user already exists.", **GLOBAL_CONTEXT)
        else:
            return render_template('auth/register.html', message="The passwords do not match.", **GLOBAL_CONTEXT)

        return redirect(url_for('login'))

    else: # Si es GET se renderiza la página register.html
        return render_template('auth/register.html', **GLOBAL_CONTEXT) # ruta de la plantilla html index


# Menú principal
@app.route('/menu')
def menu():
    # Se debe comprobar si el usuario inició sesión (cookies)
    with Session(engine) as session:
        if request.cookies.get(SESSION) != None:
            stmt = select(User).join(Cookie).where(Cookie.id == request.cookies.get(SESSION))
            user = session.scalar(stmt)
        else:
            user = None

    if user != None:
        return render_template('menu/menu.html',**GLOBAL_CONTEXT)
    else:
        return redirect(url_for('login'))


# Jugar
@app.route('/menu/play', methods=['GET', 'POST'])
def play():
    # Se debe comprobar si el usuario inició sesión (cookies)
    with Session(engine) as session:
        if request.cookies.get(SESSION) != None:
            stmt = select(User).join(Cookie).where(Cookie.id == request.cookies.get(SESSION))
            user = session.scalar(stmt)
        else:
            user = None

    # GET/POST
    if user != None:
        if request.method == 'GET':
            
            # Si para el usuario es su primera pregunta, se añade al diccionario 
            if d_score.get(user.id) == None:
                question = question_generator.generate_question()
                question_type = question['type']

                # Datos para hacer la pregunta
                url = f"{BASE_URL}/search_pokemon/{question['key']}"
                if question_type == "specific":
                    chosen_property:str = requests.get(f"{BASE_URL}/search_misc/random/{question['key']}").json()
                    url = f"{url}/{chosen_property}"
                    question["property"] = chosen_property
                    question["question"].format(X=chosen_property)
                response:Tuple[dict[str,Any],dict[str,Any]] = requests.get(url).json()
                d_score[user.id] = [0, (question,*response)]
            
            # Información de la pregunta 
            score, (question,p0,p1) =  d_score[user.id]
            
            return render_template(
                'play/play.html',
                question = question,
                name_pokemon_1 = p0["name"],
                name_pokemon_2 = p1["name"],
                img_pokemon_1 = "https://media.vozpopuli.com/2019/10/Pablo-Motos-suele-vacaciones-Javea_1295280471_13960572_660x785.png",
                img_pokemon_2 = "https://media.vozpopuli.com/2019/10/Pablo-Motos-suele-vacaciones-Javea_1295280471_13960572_660x785.png",
                # img_pokemon_1 = f"{BASE_URL}/pokemon_img/{d_score[user.id][1][1]['id']}",
                # img_pokemon_2 = f"{BASE_URL}/pokemon_img/{d_score[user.id][1][2]['id']}",
                score = score,
                **GLOBAL_CONTEXT
            )
        

        if request.method == 'POST':
            
            request.
            return render_template('play/play.html', **GLOBAL_CONTEXT)
    
    else:
        return redirect(url_for('login'))


# Pokedex
@app.route('/menu/pokedex')
def pokedex():
    # Se debe comprobar si el usuario inició sesión (cookies)
    with Session(engine) as session:
        if request.cookies.get(SESSION) != None:
            stmt = select(User).join(Cookie).where(Cookie.id == request.cookies.get(SESSION))
            user = session.scalar(stmt)
        else:
            user = None

    if user != None:
        return render_template('pokedex/pokedex.html', **GLOBAL_CONTEXT)
    else:
        return redirect(url_for('login'))
    


# Ranking
@app.route('/menu/ranking')
def ranking():
    # Se debe comprobar si el usuario inició sesión (cookies)
    with Session(engine) as session:
        if request.cookies.get(SESSION) != None:
            stmt = select(User).join(Cookie).where(Cookie.id == request.cookies.get(SESSION))
            user = session.scalar(stmt)
        else:
            user = None

    if user != None:
        top_users = [
        {'username': 'AshKetchum', 'high_score': 1500},
        {'username': 'Misty', 'high_score': 1400},
        {'username': 'Brock', 'high_score': 1350},
        {'username': 'GaryOak', 'high_score': 1300},
        {'username': 'PikachuFan', 'high_score': 1250},
        {'username': 'AshKetchum', 'high_score': 1500},
        {'username': 'Misty', 'high_score': 1400},
        {'username': 'Brock', 'high_score': 1350},
        {'username': 'GaryOak', 'high_score': 1300},
        {'username': 'PikachuFan', 'high_score': 1250},]
        user_ranking = 42 
        user_high_score = 1000
        return render_template('ranking/ranking.html', top_users=top_users, user_ranking=user_ranking, user_high_score=user_high_score)
    else:
        return redirect(url_for('login'))


# Generate a hash
def hash_gen(n:str)->str:
  return base64.b16encode(hashlib.sha512(n.encode()).digest()).decode()


# main
if __name__ == '__main__':
    app.config.from_object(config['development']) # usar configuración del diccionario definido en config.py
    app.run()
