from sqlalchemy.orm import Session
from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends

from DataBase.DB import get_db

# .env file
SECRET_KEY = "nKX6Q3Vz0fD9mA2J1pL5Ys7wTgRb8ZcMxNvKqJhCFoE="
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
db_dependency = Annotated[Session, Depends(get_db)]
