from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# # Engine with 5s statement timeout

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"options": f"-c statement_timeout={settings.DB_TIMEOUT}"}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()