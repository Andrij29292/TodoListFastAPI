from fastapi import APIRouter
from starlette import status

from . import token
from .schemas import CreateUserRequest
from DataBase.models import Users
from config import bcrypt_context, db_dependency


router = APIRouter(prefix="/auth", tags=["Authentication"])

router.include_router(token.router)

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, req: CreateUserRequest):
    model_user = Users(
        email=req.email,
        username=req.username,
        first_name=req.first_name,
        last_name=req.last_name,
        role=req.role,
        hashed_password=bcrypt_context.hash(req.password),
        is_active=True,
    )

    db.add(model_user)
    db.commit()
