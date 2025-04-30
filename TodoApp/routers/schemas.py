from pydantic import BaseModel, Field


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


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str
    complete: bool
    priority: int
    owner_id: int


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "A",
                "email": "somemail@gmail.com",
                "first_name": "Andiy",
                "last_name": "Shulla",
                "password": "1234",
                "role": "programer",
            }
        }
    }


class Token(BaseModel):
    access_token: str
    token_type: str
