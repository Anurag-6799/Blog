from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List  # Required to return a list of Pydantic models
from app.db.database import get_db
from app.schemas.posts import CreateBlog, PostResponse, PostUpdate
from app.services import posts as post_service
from app.services.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse)
def create_post_endpoint(post: CreateBlog, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """Create a new blog post."""
    return post_service.create_post(db=db, post=post, current_user=current_user)

@router.get("/", response_model=List[PostResponse])
def get_posts_endpoint(db: Session = Depends(get_db)):
    """Retrieve all blog posts."""
    return post_service.get_all_posts(db=db)

@router.put("/{post_id}", response_model=PostResponse)
def update_post_endpoint(
    post_id: int, 
    post_update: PostUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing blog post. Must be the author."""
    return post_service.update_post(db=db, post_id=post_id, post_update=post_update, current_user=current_user)


@router.delete("/{post_id}")
def delete_post_endpoint(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a blog post. Must be the author."""
    return post_service.delete_post(db=db, post_id=post_id, current_user=current_user)