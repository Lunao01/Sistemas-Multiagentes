# Archivo para configurar app.py
class DevelopmentConfig():
    DEBUG = True # modo debug para poder aplicar cambios con el servidor lanzado
    SERVER_NAME='0.0.0.0:5000'

config = {
    'development': DevelopmentConfig
}