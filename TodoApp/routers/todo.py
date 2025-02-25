from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from DataBase.DB import get_db
from DataBase.models import Todos

todo = APIRouter(prefix="/todos", tags=["Todo list"])

DB_DEPENDENCY = Annotated[Session, Depends(get_db)]

@todo.get("/all", status_code=200)
async def read_all(db: DB_DEPENDENCY):
    return db.query(Todos).all()