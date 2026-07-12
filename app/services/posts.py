from app.schemas.posts import CreateBlog
from app.db.models import User, Post
from sqlalchemy.orm import Session
from fastapi import HTTPException

def create_post(db: Session, post: CreateBlog, current_user: User):
    user = db.query(User).filter(User.user_id == post.author_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Author not found. Cannot create post.")

    db_post = Post(
        title=post.title, 
        content=post.content, 
        author_id=current_user.user_id
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return db_post

def get_all_posts(db: Session):
    # Simply retrieve all posts in the database
    return db.query(Post).all()