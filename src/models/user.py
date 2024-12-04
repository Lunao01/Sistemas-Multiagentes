# https://www.youtube.com/watch?v=XSAjQDM8ZS4
'''

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer())
    username =
    password =
    created_at = 

if __name__ == '__main__':
    pass

'''
