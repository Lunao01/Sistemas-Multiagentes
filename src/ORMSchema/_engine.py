from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine

assert load_dotenv(), "Failed to load .env file"

# docker compose up --build

DB_PASSWORD=getenv("DB_PASSWORD")
DB_USER=getenv('DB_USER') if getenv('DB_USER') is not None else 'postgres' # default user

assert DB_PASSWORD is not None, "DB_PASSWORD is not set"
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@db:5432")
# engine = create_engine('sqlite:///pokemon.db')
del DB_PASSWORD,DB_USER
