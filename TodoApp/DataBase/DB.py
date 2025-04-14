from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/todosdb"


# def create_engine_with_retry(url, max_retries=5, wait_seconds=5):
#     for retries in range(max_retries):
#         try:
#             engine = create_engine(url, echo=True)
#             engine.connect()
#             return engine
#         except Exception as e:
#             print(f"Failed to connect to the database: {e}")
#             time.sleep(wait_seconds)
#     raise Exception("Failed to connect to the database after multiple retries.")


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
