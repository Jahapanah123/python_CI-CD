from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import declarative_base

Base = declarative_base() #sqlAlchemyのモデルのベースクラス

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )