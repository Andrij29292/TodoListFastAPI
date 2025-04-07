from sqlalchemy.orm import Session
from .models import Todos
from typing import Any


class TodoWrapper:
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
