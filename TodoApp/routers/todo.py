from fastapi import APIRouter, Path, HTTPException, status, Depends
from typing import Annotated

from DataBase.models import Todos
from .schemas import TodoRequest
from config import db_dependency
from .token import get_current_user
from DataBase.wrapper import TodoWrapper

router = APIRouter(prefix="/todos", tags=["Todo list"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/all", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification Failed"
        )

    return TodoWrapper(db).get_all_todos(user.get("id"))


@router.get("/by_id/{todo_id}", status_code=status.HTTP_200_OK)
async def read_by_id(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification Failed"
        )

    model = TodoWrapper(db).get_todo_by_id(todo_id, user.get("id"))

    if model is not None:
        return model

    raise HTTPException(status.HTTP_404_NOT_FOUND, "Todo not found")


@router.post("/create/", status_code=status.HTTP_201_CREATED)
async def create_new_todo(user: user_dependency, db: db_dependency, req: TodoRequest):

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification Failed"
        )

    model = TodoWrapper(db).create_todo(req.model_dump(), owner_id_=user.get("id"))
    return model


@router.put("/update/{todo_id}")
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

    model = TodoWrapper(db).update_todo(todo_id, req.model_dump(), user.get("id"))
    
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No todo with id {todo_id} were found",
        )

    return model


@router.delete("/delete/{todo_id}")
async def delete_todo(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification Failed"
        )

    model = TodoWrapper(db).delete_todo(todo_id, user.get("id"))

    if model is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "No todo with id {todo_id} were found",
        )

    return model
