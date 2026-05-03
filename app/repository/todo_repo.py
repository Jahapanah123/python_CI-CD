from sqlalchemy.orm import Session
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate

class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: TodoCreate) -> Todo:
        db_obj = Todo(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get_by_id(self, todo_id: int) -> Todo | None:
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def get_multi(self, skip: int, limit: int) -> list[Todo]:
        return self.db.query(Todo).offset(skip).limit(limit).all()

    def update(self, db_obj: Todo, obj_in: TodoUpdate) -> Todo:
       # Convert Pydantic model to dict
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, todo_id: int) -> bool:
        db_obj = self.get_by_id(todo_id)
        if db_obj:
            self.db.delete(db_obj)
            self.db.commit()
            return True
        return False
    
    def get_by_title(self, title : str):
        return self.db.query(Todo).filter(Todo.title == title).first()