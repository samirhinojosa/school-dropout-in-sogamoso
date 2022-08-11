from sqlalchemy.ext.declarative import declarative_base
from app.configs.database import Engine

Base = declarative_base()

def init():
    Base.metadata.create_all(bind=Engine)