from flask import Flask, render_template, request, redirect, url_for
from config import config # archivo config.py
from ORMSchema import engine, User, Cookie
from sqlalchemy.orm import Session
from sqlalchemy import select
import hashlib 
import base64
import os

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
            stmt = select(User).where(User.username.is_(user)) # SELECT * FROM users WHERE username IS 'user';
            db_user = session.scalar(stmt) 

            
        if db_user is None:
            # Si el usuario no existe en la base de datos
            print("Usuario no encontrado.")
            return render_template('auth/login.html')
        
        else:
            # Verificar la contraseña usando el hash almacenado
            if db_user.password_hash == hashlib.sha512(password.encode()).digest():
                print("Login exitoso.")
                cookie = base64.b64encode(os.urandom(66))

                with Session(engine) as session:
                    # Guardar cookie
                    db_user = session.scalar(stmt)
                    db_user.cookies.append(Cookie(id = cookie)) # session.scalar(stmt) = db_user
                    session.commit()

                # Asignamos la cookie a la sesión actual
                response = redirect(url_for('menu')) 
                response.set_cookie(SESSION, cookie.decode())
                return response
            
            else:
                print("Contraseña incorrecta.")
                return render_template('auth/login.html')

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
                stmt = select(User).where(User.username.is_(user)) # SELECT * FROM users WHERE username IS 'user';
                db_user = session.scalar(stmt) 

                
                if db_user is None:
                    # Si el usuario no existe en la base de datos crea el usuario
                    print("Cuenta creada.")
                    new_user = User(username = user, password_hash = hashlib.sha512(password.encode()).digest())
                    session.add(new_user)
                    session.commit()
                
                else:
                    print("El usuario ya existe.")
        else:
            print("Las contraseñas no coinciden.")

        return redirect(url_for('login'))

    else: # Si es GET se renderiza la página register.html
        return render_template('auth/register.html') # ruta de la plantilla html index


# Menú principal
@app.route('/menu')
def menu():
    # Se debe comprobar si el usuario inició sesión (cookies)
    with Session(engine) as session:
        if request.cookies.get(SESSION) != None:
            stmt = select(User).join(Cookie).where(Cookie.id == request.cookies.get(SESSION).encode())
            user = session.scalar(stmt)
        else:
            user = None

    if user != None:
        return render_template('menu/menu.html')
    else:
        return redirect(url_for('login'))


# Jugar
@app.route('/menu/play')
def play():
    # Se debe comprobar si el usuario inició sesión (cookies)
    if True:
        return render_template('play/play.html')
    else:
        return redirect(url_for('login'))


# Pokedex
@app.route('/menu/pokedex')
def pokedex():
    # Se debe comprobar si el usuario inició sesión (cookies)
    if True:
        return render_template('pokedex/pokedex.html')
    else:
        return redirect(url_for('login'))


# main
if __name__ == '__main__':
    app.config.from_object(config['development']) # usar configuración del diccionario definido en config.py
    app.run()
