from sqlalchemy.orm import Session
from .models import Todos, Users
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from config import bcrypt_context

ModelType = TypeVar("ModelType")

class BaseWrapper(Generic[ModelType]):
    def __init__(self, db: Session, model: Type[ModelType], owner_id: Optional[int] = None):
        self.db = db
        self.model = model
        self.owner_id = owner_id

    def _get_query(self):
        query = self.db.query(self.model)
        if self.owner_id is not None and hasattr(self.model, 'owner_id'):
            query = query.filter(self.model.owner_id == self.owner_id)
        return query

    def _get_by_id(self, model_id: int):
        return self._get_query().filter(self.model.id == model_id).first()

    def _add(self, instance: ModelType) -> ModelType:
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def _update(self, instance: ModelType, update_data: Dict[str, Any]) -> ModelType:
        for key, value in update_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        self.db.merge(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def _delete(self, instance: ModelType) -> bool:
        self.db.delete(instance)
        self.db.commit()
        return True

class TodosWrapper(BaseWrapper[Todos]):
    def __init__(self, db: Session, owner_id: int):
        super().__init__(db, Todos, owner_id)

    def get_all_todos(self) -> List[Todos]:
        return self._get_query().all()

    def get_todo_by_id(self, todo_id: int) -> Optional[Todos]:
        return self._get_by_id(todo_id)

    def create_todo(self, new_todo: Dict[str, Any]) -> Todos:
        model = Todos(**new_todo, owner_id=self.owner_id)
        return self._add(model)

    def update_todo(self, todo_id: int, new_todo: Dict[str, Any]) -> Optional[Todos]:
        model = self._get_by_id(todo_id)
        if model:
            return self._update(model, new_todo)
        return None

    def delete_todo(self, todo_id: int) -> bool:
        model = self._get_by_id(todo_id)
        if model:
            return self._delete(model)
        return False

class UsersWrapper:
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, new_user: Dict[str, Any]) -> None:
        hashed_password = bcrypt_context.hash(new_user.pop('password'))
        model_user = Users(**new_user, hashed_password=hashed_password, is_active=True)
        self.db.add(model_user)
        self.db.commit()

    def get_user(self, username_: str) -> Optional[Users]:
        return self.db.query(Users).filter_by(username=username_).first()

class AdminTodosWrapper(BaseWrapper[Todos]):
    def __init__(self, db: Session):
        super().__init__(db, Todos)

    def get_all_todos(self) -> List[Todos]:
        return self._get_query().all()

    def get_todo_by_id(self, todo_id: int) -> Optional[Todos]:
        return self._get_by_id(todo_id)

    def create_todo(self, new_todo: Dict[str, Any]) -> Todos:
        model = Todos(**new_todo)
        return self._add(model)

    def update_todo(self, todo_id: int, new_todo: Dict[str, Any]) -> Optional[Todos]:
        model = self._get_by_id(todo_id)
        if model:
            return self._update(model, new_todo)
        return None

    def delete_todo(self, todo_id: int) -> bool:
        model = self._get_by_id(todo_id)
        if model:
            return self._delete(model)
        return False