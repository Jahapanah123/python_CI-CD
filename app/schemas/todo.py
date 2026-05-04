from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class TodoBase(BaseModel):
    title : str
    description : Optional[str] = None
    
# create todo ke liye
class TodoCreate(TodoBase):
    title : str = Field(..., min_length=1, max_length=100)
    description : Optional[str] = Field(None, max_length=500)

class TodoUpdate(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    is_completed : Optional[bool] = None
    
# response ke liye
class TodoResponse(TodoBase):
    id : int
    is_completed : bool
    created_at : datetime
    
    # SQLAlchemy object support
    model_config = ConfigDict(from_attributes=True)
    