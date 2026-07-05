import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url, connect_args={"sslmode": "require"})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

class Base(DeclarativeBase):
    pass

# Dependency to yield database sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
