import json
from typing import Any, List, Tuple
from urllib.parse import unquote
from flask import Flask, render_template, request, redirect, url_for
from config import config # archivo config.py
from ORMSchema import engine, User, Cookie, GrowthRate, Score
from sqlalchemy.orm import Session
from sqlalchemy import select
import hashlib 
import base64
import os
import question_generator 
import requests

app = Flask(__name__)
SESSION = "session"
REST_API_URL = "http://rest_api:8000"
REST_API_CLIENT_URL = "http://localhost:8000"
d_score:dict[int,Any] = dict() # Guardar el puntaje del usuario en la partida
GLOBAL_CONTEXT = {
    "base_url": "http://localhost:5000",
}
FAIL_REDIR = -1

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
            user_id = user.id
        else:
            user = None

    # GET/POST
    if user != None:
        if request.method == 'GET':
            return play_get(user_id) # cant be unbound, since if user != none implies that conditional in line 126 was run

        if request.method == 'POST':
            if 'exit' in request.args.keys():
                del d_score[user_id]
                return ''
            
            question = request.args.to_dict()
            del question['pokemon1']
            del question['pokemon2']
            del question['pokemon_guess']

            _poke1:requests.Response = requests.get(f"{REST_API_URL}/pokemon/{request.args['pokemon1']}")
            if _poke1.status_code == 404:
                ERRMSG = "404 pokemon not found. This is an internal server error, please report this issue to the devs"
                return render_template('play/play.html', message = ERRMSG,**GLOBAL_CONTEXT)
            assert _poke1.status_code == 200
            poke1:dict[str,str|int|bool|List[str]|GrowthRate]=_poke1.json()
            del _poke1
                
            
            _poke2:requests.Response = requests.get(f"{REST_API_URL}/pokemon/{request.args['pokemon2']}")
            if _poke2.status_code == 404:
                ERRMSG = "404 pokemon not found. This is an internal server error, please report this issue to the devs"
                return render_template('play/play.html', message = ERRMSG,**GLOBAL_CONTEXT)
            assert _poke2.status_code == 200
            poke2:dict = _poke2.json()
            del _poke2

            _poke_guess:requests.Response = requests.get(f"{REST_API_URL}/pokemon/{request.args['pokemon_guess']}")
            if _poke_guess.status_code == 404:
                ERRMSG = "404 pokemon not found. This is an internal server error, please report this issue to the devs"
                return render_template('play/play.html', message = ERRMSG,**GLOBAL_CONTEXT)
            assert _poke_guess.status_code == 200
            poke_guess:dict = _poke_guess.json()
            del _poke_guess

            correct = False
            poke_a = poketest(poke1,poke2,question)
            poke_guess['id'] == poke_a
            if question['type'] == 'compare':
                if poke1[question['key']] < poke2[question['key']]:
                    if poke_guess['id']==poke1['id']:
                        correct = question['condition']=='less'
                    elif poke_guess['id']==poke2['id']:
                        correct = question['condition']=='more'
                    else:
                        raise Exception()
                elif poke1[question['key']] > poke2[question['key']]:                        
                    if poke_guess['id']==poke1['id']:
                        correct = question['condition']=='more'
                    elif poke_guess['id']==poke2['id']:
                        correct = question['condition']=='less'
                    else:
                        raise Exception()
                elif poke1[question['key']] == poke2[question['key']]:
                    if poke_guess['id']==poke1['id'] or poke_guess['id'] == poke2['id']:
                        correct = True
                    else:
                        raise Exception()
            elif question['type'] == 'specific':
                r = []
                if question['property'] in poke1[question['key']]:
                    r.append(poke1['id'])
                if question['property'] in poke2[question['key']]:
                    r.append(poke2['id'])
                if poke_guess['id'] in r:
                    correct = True
            elif question['type'] == 'choice':
                if poke1[question['key']]:
                    r = poke1
                elif poke2[question['key']]:
                    r = poke2
                else:
                    raise Exception("Unreachable code")
                
                if r['id'] == poke_guess['id']:
                    correct = True
            else:
                raise Exception("Guessed invalid question (Nonexistant type).")
            
            if correct:
                gen_question(user_id)
                d_score[user_id][0] += 1
                return play_get(user_id)
            else:
                p = d_score[user_id][0]
                d_score[user_id] = FAIL_REDIR
                with Session(engine) as session:
                    stmt = select(User).where(User.id == user_id)
                    u = session.execute(stmt).first()
                    assert u is not None
                    u = u.tuple()[0]
                    u.scores.append(Score(score=p))
                return ""
                
    
    else:
        return redirect(url_for('login'))


def play_get(user_id):
    # Si para el usuario es su primera pregunta, se añade al diccionario 
    if d_score.get(user_id) == None:
        d_score[user_id] = [0, None]
        gen_question(user_id)
    if d_score.get(user_id) == FAIL_REDIR:
        del d_score[user_id]
        return redirect(url_for('menu/end_screen'))
    
    # Información de la pregunta 
    score, (question,p0,p1) =  d_score[user_id]
    
    return render_template(
        'play/play.html',
        question = question,
        pokemon_1 = p0,
        pokemon_2 = p1,
        pokemon_a = None, # TODO
        img_pokemon_1 = f"{REST_API_CLIENT_URL}/pokemon_img/{d_score[user_id][1][1]['id']}",
        img_pokemon_2 = f"{REST_API_CLIENT_URL}/pokemon_img/{d_score[user_id][1][2]['id']}",
        score = score,
        **GLOBAL_CONTEXT
    )

def poketest(p0,p1,q):
    if q['type'] == 'compare':
        if q['condition'] == 'less':
            if p0[q['key']] < p1[q['key']]:
                return p0
            if p0[q['key']] > p1[q['key']]:
                return p1
        if q['condition'] == 'more':
            if p0[q['key']] < p1[q['key']]:
                return p1
            if p0[q['key']] > p1[q['key']]:
                return p0
    elif q['type'] == 'specific':
        if q['property'] in p0[q['key']]:
            return p0
        if q['property'] in p1[q['key']]:
            return p1
    elif q['type'] == 'choice':
        if p0[q['key']] == True:
            return p0
        if p1[q['key']] == True:
            return p1

    raise Exception("Unreachable code")

def gen_question(user_id):
    question = question_generator.generate_question()
    question_type = question['type']
    # Datos para hacer la pregunta
    url = f"{REST_API_URL}/search_pokemon/{question['key']}"
    if question_type == "specific":
        chosen_property:str = requests.get(f"{REST_API_URL}/search_misc/random/{question['key']}").json()
        url = f"{url}/{chosen_property}"
        question["property"] = chosen_property
        question["question"].format(X=chosen_property)
    response:Tuple[dict[str,Any],dict[str,Any]] = requests.get(url).json()
    d_score[user_id][1] = (question,*response)

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
        

        '''top_users = [
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
        user_high_score = 1000'''


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
