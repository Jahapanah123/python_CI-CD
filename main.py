from fastapi import FastAPI
from app.api.todo_handler import router as todo_router
from app.db.session import engine
from app.models import todo as todo_model

# Database tables create karne ke liye (Simple setup)
todo_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")

# Router registration
app.include_router(todo_router)

@app.get("/")
def health_check():
    return {"status": "API is running!"}