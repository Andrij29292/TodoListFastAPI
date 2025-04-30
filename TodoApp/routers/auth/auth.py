from fastapi import APIRouter
from starlette import status

from . import token
from ..schemas import CreateUserRequest
from ...DataBase.wrapper import UsersWrapper
from ...config import db_dependency


router = APIRouter(prefix="/auth", tags=["Authentication"])

router.include_router(token.router)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, req_user: CreateUserRequest):
    UsersWrapper(db).add_user(req_user.model_dump())
