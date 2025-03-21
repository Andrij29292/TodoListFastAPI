from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DB_URL = "sqlite:///./todosapp.db"

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})

SsesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SsesionLocal()
    try:
        yield db
    finally:
        db.close()
    
