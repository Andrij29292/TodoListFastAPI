from sqlalchemy.orm import Session
from .models import Todos, Users
from typing import Any
from config import bcrypt_context


class DataBaseWrapper:
    def __init__(self, db: Session):
        self.db = db

    def get_all_todos(self, owner_id):
        return self.db.query(Todos).filter(Todos.owner_id == owner_id).all()

    def get_todo_by_id(self, todo_id, owner_id_):
        return (
            self.db.query(Todos)
            .filter(Todos.id == todo_id)
            .filter(Todos.owner_id == owner_id_)
            .first()
        )

    def create_todo(self, new_todo: dict[str, Any], owner_id_):
        model = Todos(**new_todo, owner_id=owner_id_)
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return model

    def update_todo(self, todo_id, new_todo: dict[str, Any], owner_id_):
        model = (
            self.db.query(Todos)
            .filter(Todos.id == todo_id)
            .filter(Todos.owner_id == owner_id_)
            .first()
        )

        if model is None:
            return model

        model.title = new_todo["title"]
        model.description = new_todo["description"]
        model.priority = new_todo["priority"]
        model.complete = new_todo["complete"]

        self.db.merge(model)
        self.db.commit()
        self.db.refresh(model)

        return model

    def delete_todo(self, todo_id, user_id):
        is_delete = (
            self.db.query(Todos)
            .filter(Todos.id == todo_id, Todos.owner_id == user_id)
            .delete()
        )
        self.db.commit()
        return bool(is_delete)

    def add_user(self, new_user: dict[str, Any]):
        model_user = Users(
            email=new_user['email'],
            username=new_user["username"],
            first_name=new_user["first_name"],
            last_name=new_user["last_name"],
            role=new_user["role"],
            hashed_password=bcrypt_context.hash(new_user["password"]),
            is_active=True,
        )

        self.db.add(model_user)
        self.db.commit()

    def get_user(self, username_: str):
        return self.db.query(Users).filter_by(username=username_).first()
