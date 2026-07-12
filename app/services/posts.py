from app.schemas.posts import CreateBlog
from app.db.models import User, Post
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

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


def update_post(db: Session, post_id: int, post_update: PostUpdate, current_user: User):
    # 1. Fetch the post
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    # 2. Check if it exists
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    # 3. AUTHORIZATION CHECK: Does the current user own this post?
    if db_post.author_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this post")

    # 4. Apply updates only for fields that were provided
    if post_update.title is not None:
        db_post.title = post_update.title
    if post_update.content is not None:
        db_post.content = post_update.content

    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int, current_user: User):
    # 1. Fetch the post
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    # 2. Check if it exists
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
    # 3. AUTHORIZATION CHECK: Does the current user own this post?
    if db_post.author_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this post")

    # 4. Delete the record
    db.delete(db_post)
    db.commit()
    return {"detail": "Post deleted successfully"}


