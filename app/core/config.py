import os

from dotenv import load_dotenv

# env file ko load karna
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DB_TIMEOUT: int = int(os.getenv("DB_TIMEOUT", 5000))  
    
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL missing! Check your .env file.")
    
settings = Settings()