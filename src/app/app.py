import json
from typing import Any, List
from urllib.parse import unquote
from flask import Flask, render_template, request, redirect, url_for
from config import config # archivo config.py
from ORMSchema import engine, User, Cookie, GrowthRate, Score, Pokemon
from sqlalchemy.orm import Session
from sqlalchemy import alias, column, desc, func, select
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
        with Session(engine) as session:
            if request.cookies.get(SESSION) != None:
                stmt = select(Cookie).where(Cookie.id == request.cookies.get(SESSION))
                c = session.execute(stmt).first()
                if c == None:
                    return render_template('auth/login.html',**GLOBAL_CONTEXT) # ruta de la plantilla html index
                else:
                    return redirect(url_for('menu'))
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
            user = session.execute(stmt).first()
            user = user[0]
            if user != None:
                user_id = user.id
        else:
            user = None

    if user != None:
        if request.args.get('logout') != None:
            with Session(engine) as session:
                stmt = select(User).where(User.id == user_id)
                _user = session.execute(stmt).first()
                assert _user!=None
                user = _user[0]
                del _user
                for n,c in enumerate(user.cookies):
                    if request.cookies.get(SESSION) ==  c.id:
                        user.cookies.pop(n)
                session.commit()
            return redirect(url_for('login'))
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
            user = session.execute(stmt).first()
            user = user[0]
            if user != None:
                user_id = user.id
        else:
            user = None

    # GET/POST
    if user != None:
        if request.method == 'GET':
            return play_get(user_id) # cant be unbound, since if user != none implies that conditional in line 126 was run

        if request.method == 'POST':
            
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
            if poke_guess['id'] in poke_a:
                d_score[user_id][1] = gen_question(user_id)
                d_score[user_id][0] += 1

                # Desbloquear pokemon:
                with Session(engine) as session:
                    if request.cookies.get(SESSION) != None:
                        # Pokémon desbloqueado
                        stmt = select(Pokemon).where(poke_guess['id'] == Pokemon.id)
                        pokemon = session.scalar(stmt)

                        # Usuario de la sesión
                        stmt = select(User).where(User.id == user_id)
                        user = session.scalar(stmt)
                
                        user.unlocked_pokemon.append(pokemon)

                    session.commit()

                return play_get(user_id)
            else:
                p = d_score[user_id][0]
                del d_score[user_id]
                with Session(engine) as session:
                    stmt = select(User).where(User.id == user_id)
                    u = session.execute(stmt).first()
                    assert u is not None
                    u = u[0]
                    u.scores.append(Score(score=p))
                    session.commit()
                return render_template("play/you_lose.html", score=p)
                
    
    else:
        return redirect(url_for('login'))


def play_get(user_id):
    if 'new_game' in request.args.keys() and d_score.get(user_id) != None:
        del d_score[user_id]
    # Si para el usuario es su primera pregunta, se añade al diccionario 
    if d_score.get(user_id) == None:
        d_score[user_id] = [0, gen_question(user_id)]
    # if d_score.get(user_id)[1] == None:
    #     score = d_score.get(user_id)[0]
    #     del d_score[user_id]
    #     return render_template('play/you_lose.html', score = score)
    
    # Información de la pregunta 
    score, (question,p0,p1) =  d_score[user_id]
    if question['type']=='specific':
        question['question'] = question['question'].format(X=question['property'])
    
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

def poketest(p0:dict[str,Any],p1:dict[str,Any],q:dict[str,Any]) -> tuple:
    if q['type'] == 'compare':
        if q['condition'] == 'less':
            if p0[q['key']] < p1[q['key']]:
                return (p0['id'],)
            elif p0[q['key']] > p1[q['key']]:
                return (p1['id'],)
            else: # p0[q['key']] == p1[q['key']]
                return (p0['id'],p1['id'])
        if q['condition'] == 'more':
            if p0[q['key']] < p1[q['key']]:
                return (p1['id'],)
            elif p0[q['key']] > p1[q['key']]:
                return (p0['id'],)
            else: # p0[q['key']] == p1[q['key']]
                return (p0['id'],p1['id'])
    elif q['type'] == 'specific':
        if q['property'] in p0[q['key']]:
            return (p0['id'],)
        elif q['property'] in p1[q['key']]:
            return (p1['id'],)
        else:
            raise Exception("Unreachable code. Neither of the pokemons were valid (or both were).")
    elif q['type'] == 'choice':
        if p0[q['key']] == True and p1[q['key']] == False:
            return (p0['id'],)
        elif p1[q['key']] == True and p0[q['key']] == False:
            return (p1['id'],)
        else:
            raise Exception("Unreachable code. Neither of the pokemons were valid (or both were).")
    else:
        raise Exception("Unreachable code. Invalid question")

def gen_question(user_id):
    question = question_generator.generate_question()
    question_type = question['type']
    # Datos para hacer la pregunta
    url = f"{REST_API_URL}/search_pokemon/{question['key']}"
    if question_type == "specific":
        _chosen_property = requests.get(f"{REST_API_URL}/search_misc/random/{question['key']}")
        if _chosen_property.status_code != 200:
            raise Exception(f"API Call to {REST_API_URL}/search_misc/random/{question['key']} returned status code {_chosen_property.status_code}.")
        chosen_property:str = _chosen_property.json()
        del _chosen_property

        url = f"{url}/{chosen_property}"
        question["property"] = chosen_property
        question["question"].format(X=chosen_property)
    _response = requests.get(url)
    if _response.status_code != 200:
        raise Exception(f"API Call to {url} returned status code {_response.status_code}.")
    response:tuple[dict[str,Any],dict[str,Any]] = _response.json()
    assert len(response) == 2
    return (question,*response)

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
            pokemon_selected_id = request.args.to_dict().get('pokemon_selected')
            
            # Buscamos los pokemon desbloqueados por el usuario
            unlocked_pokemon_list = []
            for p in user.unlocked_pokemon:
                pokemon_img = f"{REST_API_CLIENT_URL}/pokemon_img/{p.id}"
                unlocked_pokemon_list.append([p.id, p.name, pokemon_img])

            return render_template('pokedex/pokedex.html', unlocked_pokemon_list=unlocked_pokemon_list, pokemon_selected_id = pokemon_selected_id)
        
        else:
            return redirect(url_for('login'))
        
# Pokedex/Pokemon
@app.route('/menu/pokedex/data')
def pokemon_info():
    # Se debe comprobar si el usuario inició sesión (cookies)
    with Session(engine) as session:
        if request.cookies.get(SESSION) != None:
            stmt = select(User).join(Cookie).where(Cookie.id == request.cookies.get(SESSION))
            user = session.execute(stmt).first()
        else:
            user = None

        if user != None:
            # Buscamos el pokemon en la base de datos
            stmt = select(Pokemon).where(Pokemon.id == request.args['pokemon_id'])
            pokemon = session.scalar(stmt)
            
            # Control para que los usuarios no pongan números absurdos 
            if pokemon == None:
                return redirect(url_for('pokedex'))
            
            # Imagen del pokemon
            img_pokemon = f"{REST_API_CLIENT_URL}/pokemon_img/{pokemon.id}",
            

            # Ajustamos el formato de mensaje para types, habitat y abilities
            if len(pokemon.types) > 0:
                type_msg = ""
                for i in pokemon.types[:-1]:
                    type_msg += f"{i.type}, "
                type_msg += f"{pokemon.types[-1].type}"
            else:
                type_msg = "Undefined."


            if len(pokemon.habitat) > 0:
                habitat_msg = ""
                for i in pokemon.habitat[:-1]:
                    habitat_msg += f"{i.habitat}, "
                habitat_msg += f"{pokemon.habitat[-1].habitat}"
            else:
                habitat_msg = "Undefined."

            if len(pokemon.abilities) > 0:
                abilities_msg = ""
                for i in pokemon.abilities[:-1]:
                    abilities_msg += f"{i.ability}, "
                abilities_msg += f"{pokemon.abilities[-1].ability}"
            else:
                abilities_msg = "Undefined."


            # Calculamos el mejor valor en cada estadística
            stmt = select(Pokemon).order_by(Pokemon.hp.desc()).limit(1)
            pokemon_with_highest_hp = session.scalar(stmt)

            stmt = select(Pokemon).order_by(Pokemon.attack.desc()).limit(1)
            pokemon_with_highest_attack = session.scalar(stmt)

            stmt = select(Pokemon).order_by(Pokemon.defense.desc()).limit(1)
            pokemon_with_highest_defense = session.scalar(stmt)

            stmt = select(Pokemon).order_by(Pokemon.special_attack.desc()).limit(1)
            pokemon_with_highest_special_attack = session.scalar(stmt)

            stmt = select(Pokemon).order_by(Pokemon.special_defense.desc()).limit(1)
            pokemon_with_highest_special_defense = session.scalar(stmt)

            stmt = select(Pokemon).order_by(Pokemon.speed.desc()).limit(1)
            pokemon_with_highest_speed = session.scalar(stmt)
            
            # Porcentaje para el diagrama de barras en la info del pokemon
            hp = int((pokemon.hp/pokemon_with_highest_hp.hp)*100)
            attack = int((pokemon.attack/pokemon_with_highest_attack.attack)*100)
            defense = int((pokemon.defense/pokemon_with_highest_defense.defense)*100)
            special_attack = int((pokemon.special_attack/pokemon_with_highest_special_attack.special_attack)*100)
            special_defense = int((pokemon.special_defense/pokemon_with_highest_special_defense.special_defense)*100)
            speed = int((pokemon.speed/pokemon_with_highest_speed.speed)*100)



            return render_template('pokedex/pokedex_info.html',img=img_pokemon, id=pokemon.id, name=pokemon.name, type=type_msg, height=pokemon.height, weight=pokemon.weight, habitat=habitat_msg, abilities=abilities_msg, legendary=pokemon.is_legendary, hp=hp, attack=attack, defense=defense, special_attack=special_attack, special_defense=special_defense, speed=speed)
        else:
            return redirect(url_for('login'))

# Ranking
@app.route('/menu/ranking')
def ranking():
    # Se debe comprobar si el usuario inició sesión (cookies)

    with Session(engine) as session:
        if request.cookies.get(SESSION) != None:
            stmt = select(User).join(Cookie).where(Cookie.id == request.cookies.get(SESSION))
            user = session.execute(stmt).first()
            if user==None:
                user_found=False
            else:
                user=user[0]
                
                user_high_score=max(map(lambda x:x.score,user.scores),default=0)
                stmt_rank_ms = func.max(Score.score)
                stmt_rank = (
                    # select(column("ranking"))
                    # .select_from(
                        select(User.id.label("user_id"),User.username, func.rank().over(order_by=desc(stmt_rank_ms)).label("ranking"),stmt_rank_ms)
                        .join(Score, Score.user_id == User.id)
                        .group_by(User.id)
                        .order_by(desc(stmt_rank_ms))
                    # )
                    # .where(column("user_id") == user.id)
                )
                # HACK i wanted to do the previous one with sql views, but sqlalchemy didnt seem to support it, 
                # and i couldn't think of a better way, so for now, it will conver the ranking of all users into 
                # a dict, and look up the current user there. Even if this is not a scalable solution, it should be fine for our use-case
                ranking:dict[int,int] = dict(map(lambda x: (x[0],x[2]),session.execute(stmt_rank).all()))
                user_ranking = ranking[user.id]
                top_users:list[dict[str,str|int]] = list(map(lambda x:{'username':x[1],'high_score':x[3]},session.execute(stmt_rank.limit(10)).all()))

                user_found=True

        else:
            user_found=False
        del user, stmt

    if user_found:
        return render_template('ranking/ranking.html', top_users=top_users, user_ranking=user_ranking, user_high_score=user_high_score)
    else:
        return redirect(url_for('login'))

# Lose menu
@app.route('/menu/play/lose')
def lose():
    # Se debe comprobar si el usuario inició sesión (cookies)
    with Session(engine) as session:
        if request.cookies.get(SESSION) != None:
            stmt = select(User).join(Cookie).where(Cookie.id == request.cookies.get(SESSION))
            user = session.scalar(stmt)
        else:
            user = None

    if user != None:
        return render_template('play/you_lose.html')
    else:
        return redirect(url_for('login'))


# Generate a hash
def hash_gen(n:str)->str:
  return base64.b16encode(hashlib.sha512(n.encode()).digest()).decode()


# main
if __name__ == '__main__':
    app.config.from_object(config['development']) # usar configuración del diccionario definido en config.py
    app.run()
