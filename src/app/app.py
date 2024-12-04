from flask import Flask, render_template, request, redirect, url_for
from config import config # archivo config.py

app = Flask(__name__)

# db = MySQL(app)

# Nada más cargar la ruta raíz te reenvia a /login
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username']) # username del formulario
        print(request.form['password']) # password del formulario
        return redirect(url_for('menu'))

    else: # Si es GET se renderiza la página login.html
        return render_template('auth/login.html') # ruta de la plantilla html index

@app.route('/menu')
def menu():
    return render_template('menu/menu.html')


if __name__ == '__main__':
    app.config.from_object(config['development']) # usar configuración del diccionario definido en config.py
    app.run()
