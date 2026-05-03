from app.repository.base import TodoRepositoryProto
from app.schemas.todo import TodoCreate, TodoUpdate
from utils import errors

class TodoService:
    def __init__(self, repo: TodoRepositoryProto):
        self.repo = repo

    def create_task(self, data: TodoCreate):
        clean_title = data.title.strip()
        if clean_title == "":
            raise errors.ValidationError("Title cannot be empty")
        
        # duplicate title check 
        existing = self.repo.get_by_title(title = clean_title)
        if existing:
            raise errors.ConflictError({"message":"Task already exists", "title": existing.title})
        return self.repo.create(data)

    def get_task(self, todo_id: int):
        if todo_id <= 0:
            raise errors.ValidationError("ID must be positive")
        task = self.repo.get_by_id(todo_id)
        if not task:
            raise errors.NotFoundError(f"Task {todo_id} not found")
        return task

    def list_tasks(self, skip: int = 0, limit: int = 10):
        # Business Logic: Max limit enforcement
        if skip < 0 or limit <= 0:
            raise errors.ValidationError("Skip must be non-negative and limit must be positive")
        safe_limit = min(limit, 100)  
        return self.repo.get_multi(skip=skip, limit=safe_limit)

    def update_task(self, todo_id: int, data: TodoUpdate):
       task = self.get_task(todo_id)  
       #duplicate title check
       if data.title is not None:
            clean_title = data.title.strip()
            if clean_title == "":
                raise errors.ValidationError("Title cannot be empty")
            
            
            existing = self.repo.get_by_title(title = clean_title)
            if existing and existing.id != todo_id:
                raise errors.ConflictError(f"A task with {existing.title} already exists")
            data.title = clean_title
       return self.repo.update(task, data)
     
    def remove_task(self, todo_id: int):
        task = self.get_task(todo_id)
        return self.repo.delete(todo_id)