from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List  # Required to return a list of Pydantic models
from app.db.database import get_db
from app.schemas.posts import CreateBlog, PostResponse
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