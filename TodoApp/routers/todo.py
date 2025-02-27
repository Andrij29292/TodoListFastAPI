from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from DataBase.DB import get_db
from DataBase.models import Todos

todo = APIRouter(prefix="/todos", tags=["Todo list"])

DB_DEPENDENCY = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(..., max_length=50)
    description: str = Field(..., max_length=100)
    priority: int = Field(gt=0, le=5)
    complete: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "New title",
                "description": "New descriprion",
                "priority": 5,
                "complete": False,
            }
        }
    }


@todo.get("/all", status_code=status.HTTP_200_OK)
async def read_all(db: DB_DEPENDENCY):
    return db.query(Todos).all()


@todo.get("/by_id/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(db: DB_DEPENDENCY, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status.HTTP_404_NOT_FOUND, "Todo not found")


@todo.post("/create/", status_code=status.HTTP_201_CREATED)
async def create_new_todo(db: DB_DEPENDENCY, req: TodoRequest):
    model = Todos(**req.model_dump())

    db.add(model)
    db.commit()


@todo.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: DB_DEPENDENCY,
    req: TodoRequest,
    todo_id: int = Path(gt=0),
):
    model = db.query(Todos).filter(Todos.id == todo_id).first()

    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No todo with id {todo_id} were found",
        )

    model.title = req.title
    model.description = req.description
    model.priority = req.priority
    model.complete = req.complete

    db.merge(model)
    db.commit()
