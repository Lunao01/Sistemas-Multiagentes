# Archivo para configurar app.py
class Config:
    SECRET_KEY = 'S8!}.Nz=_ba?@v5QPdcZ\^5a,Y>],F'

class DevelopmentConfig(Config):
    DEBUG = True # modo debug para poder aplicar cambios con el servidor lanzado
    MYSQL_HOST = 'localhost' # host
    MYSQL_USER = 'root' # usuario 
    MYSQL_PASSWORD = '123456' # password
    MYSQL_DB = 'poke_quest' # nombre de la base de datos

config = {
    'development': DevelopmentConfig
}