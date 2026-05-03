from typing import Protocol, TypeVar, Any, Optional, List
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

# Generic Type for flexibility if needed later
T = TypeVar("T")

class CreateRepository(Protocol):
    def create(self, obj_in: Any) -> Any: ...

class ReadRepository(Protocol):
    def get_by_id(self, id: int) -> Optional[Any]: ...
    def get_multi(self, skip: int, limit: int) -> List[Any]: ...

class UpdateRepository(Protocol):
    def update(self, db_obj: Any, obj_in: Any) -> Any: ...

class DeleteRepository(Protocol):
    def delete(self, id: int) -> bool: ...

# Combined interface for Todo (The one Service will use)
class TodoRepositoryProto(
    CreateRepository, 
    ReadRepository, 
    UpdateRepository, 
    DeleteRepository, 
    Protocol
):
    pass