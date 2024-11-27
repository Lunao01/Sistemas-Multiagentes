from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine

assert load_dotenv(), "Failed to load .env file"
DB_PASSWORD=getenv("DB_PASSWORD")
DB_USER=getenv('DB_USER') if getenv('DB_USER') is not None else 'postgres' # default user

assert DB_PASSWORD is not None, "DB_PASSWORD is not set"
engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/pokemon")
del DB_PASSWORD,DB_USER
