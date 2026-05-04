from typing import Protocol, List, Optional, Any
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

class CreateRepository(Protocol):
    def create(self, obj_in: Any) -> Todo: ...

class ReadRepository(Protocol):
    def get_by_id(self, todo_id: int) -> Todo | None: ...
    def get_multi(self, skip: int, limit: int) -> list[Todo]: ...

class UpdateRepository(Protocol):
    def update(self, db_obj: Any, obj_in: Any) -> Todo: ...

class DeleteRepository(Protocol):
    def delete(self, todo_id: int) -> bool: ...

# Combined interface for Todo (The one Service will use)
class TodoRepositoryProto(
    CreateRepository, 
    ReadRepository, 
    UpdateRepository, 
    DeleteRepository, 
    Protocol
):
    pass