from pydantic import BaseModel, Field
from DataBase.models import Todos


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


class TodoResponse:
    def __init__(self, response_model: Todos):
        self.id = response_model.id
        self.title = response_model.title
        self.description = response_model.description
        self.complete = response_model.complete
        self.priority = response_model.priority
        self.owner_id = response_model.owner_id


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
                "username": "Andrii29292",
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
