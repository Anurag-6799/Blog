from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.database import Base
import uuid

def generate_user_id():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(String(36), primary_key=True, index=True, default=generate_user_id)
    user_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    posts = relationship("Post", back_populates="author") 


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=lambda: int(datetime.now(timezone.utc).timestamp()))
    
    # Foreign Key linking to the User table
    author_id = Column(String(36), ForeignKey("users.user_id"))

    # Relationship back to the User table
    author = relationship("User", back_populates="posts")
    