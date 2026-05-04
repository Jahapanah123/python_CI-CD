from app.schemas.todo import TodoCreate, TodoUpdate
from utils import errors
from app.services.protocol import TodoRepositoryProto

class TodoService:
    def __init__(self, repo: TodoRepositoryProto):
        self.repo = repo

    async def create_task(self, data: TodoCreate):
        clean_title = data.title.strip()
        if clean_title == "":
            raise errors.ValidationError("Title cannot be empty")
        
        # duplicate title check 
        existing = await self.repo.get_by_title(title = clean_title)
        if existing:
            raise errors.ConflictError(f"task with title '{existing.title}' already exists")
        clean_title = data.title # upar strip k bad client k given spaces hat jate h so define the title again with original
        return await self.repo.create(data)

    async def get_task(self, todo_id: int):
        if todo_id <= 0:
            raise errors.ValidationError("ID must be positive")
        task = await self.repo.get_by_id(todo_id)
        if not task:
            raise errors.NotFoundError(f"Task {todo_id} not found")
        return task

    async def list_tasks(self, skip: int = 0, limit: int = 10):
        # Business Logic: Max limit enforcement
        if skip < 0 or limit <= 0:
            raise errors.ValidationError("Skip must be non-negative and limit must be positive")
        safe_limit = min(limit, 100)  
        return await self.repo.get_multi(skip=skip, limit=safe_limit)

    async def update_task(self, todo_id: int, data: TodoUpdate):
       task = await self.get_task(todo_id)  
       #duplicate title check
       if data.title is not None:
            clean_title = data.title.strip()
            if clean_title == "":
                raise errors.ValidationError("Title cannot be empty")
            
            existing = await self.repo.get_by_title(title = clean_title)
            if existing and existing.id != todo_id:
                raise errors.ConflictError(f"A task with {existing.title} already exists")
            data.title = clean_title
            
       if data.description is not None:
            clean_description = data.description.strip()
            if len(clean_description) > 500:
                raise errors.ValidationError("Description cannot be longer than 500 characters")
            data.description = clean_description
            return await self.repo.update(task, data) 
     
    async def remove_task(self, todo_id: int):
        task = await self.get_task(todo_id)
        await self.repo.delete(task)
        return {"message": f"Task {todo_id} deleted successfully"}