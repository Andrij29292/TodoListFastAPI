from fastapi import APIRouter, Path, HTTPException, status, Depends
from typing import Annotated

from DataBase.models import Todos
from .schemas import TodoRequest
from config import db_dependency
from .token import get_current_user


router = APIRouter(prefix="/todos", tags=["Todo list"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/all", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification Failed"
        )
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/by_id/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification Failed"
        )

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is not None:
        return todo_model

    raise HTTPException(status.HTTP_404_NOT_FOUND, "Todo not found")


@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def create_new_todo(user: user_dependency, db: db_dependency, req: TodoRequest):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification Failed"
        )

    model = Todos(**req.model_dump(), owner_id=user.get("id"))

    db.add(model)
    db.commit()


@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    req: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification Failed"
        )

    model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

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


@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification Failed"
        )

    model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

    if model is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "No todo with id {todo_id} were found",
        )

    db.query(Todos).filter_by(id=todo_id).delete()
    db.commit()
