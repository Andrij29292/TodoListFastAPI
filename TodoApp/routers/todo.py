from fastapi import APIRouter, Path, HTTPException, status, Depends
from typing import Annotated

from .schemas import TodoRequest, TodoResponse
from config import db_dependency
from .token import get_current_user
from DataBase.wrapper import DataBaseWrapper

user_dependency = Annotated[dict, Depends(get_current_user)]

router = APIRouter(
    prefix="/todos",
    tags=["Todo list"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/all",
    response_model=list[TodoResponse],
    status_code=status.HTTP_200_OK,
)
async def read_all(user: user_dependency, db: db_dependency):
    return [todo for todo in DataBaseWrapper(db).get_all_todos(user.get("id"))]


@router.get(
    "/by_id/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
async def read_by_id(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0),
):
    model = DataBaseWrapper(db).get_todo_by_id(todo_id, user.get("id"))

    if model is not None:
        return model

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Todo not found")


@router.post(
    "/create/",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_new_todo(
    user: user_dependency,
    db: db_dependency,
    req: TodoRequest,
):
    model = DataBaseWrapper(db).create_todo(req.model_dump(), owner_id_=user.get("id"))
    return model


@router.put(
    "/update/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_req: TodoRequest,
    todo_id: int = Path(gt=0),
):
    model = DataBaseWrapper(db).update_todo(
        todo_id, todo_req.model_dump(), user.get("id")
    )

    if model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No todo with id {todo_id} were found",
        )

    return model


@router.delete(
    "/delete/{todo_id}",
    status_code=status.HTTP_200_OK,
)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0),
):
    if not DataBaseWrapper(db).delete_todo(todo_id, user.get("id")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No todo with id {todo_id} were found",
        )
