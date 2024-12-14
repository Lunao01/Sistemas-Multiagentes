from flask import Flask, render_template, request, redirect, url_for
from config import config # archivo config.py
from ORMSchema import engine, User, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import select
import hashlib 
import base64
import os
import question_generator 

app = Flask(__name__)
SESSION = "session"

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
            return render_template('auth/login.html', message="User not found.")
        
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
                return render_template('auth/login.html', message="Incorrect password.")

    else: # Si es GET se renderiza la página login.html
        return render_template('auth/login.html') # ruta de la plantilla html index


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
                    return render_template('auth/login.html', message="The user already exists.")
        else:
            return render_template('auth/login.html', message="The passwords do not match.")

        return redirect(url_for('login'))

    else: # Si es GET se renderiza la página register.html
        return render_template('auth/register.html') # ruta de la plantilla html index


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
        return render_template('menu/menu.html')
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
        # Se genera la pregunta
        question = question_generator.generate_question()
        question_text = question.question
        question_key = question.key
        question_type = question.type

        if question_type == "compare":
            pass
        elif question_type == "choice":
            pass
        elif question_type == "abilities":
            pass

        if request.method == 'GET':
            return render_template('play/play.html')
        

        if request.method == 'POST':
            return render_template('play/play.html')
    
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
        return render_template('pokedex/pokedex.html')
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
        return render_template('ranking/ranking.html')
    else:
        return redirect(url_for('login'))


# Generate a hash
def hash_gen(n:str)->str:
  return base64.b16encode(hashlib.sha512(n.encode()).digest()).decode()


# main
if __name__ == '__main__':
    app.config.from_object(config['development']) # usar configuración del diccionario definido en config.py
    app.run()
