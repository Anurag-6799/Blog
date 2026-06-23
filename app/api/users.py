from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schema.user import UserCreate, UserResponse
from app.services import user as user_service

# Create a router specifically for user-related endpoints
router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user. 
    FastAPI automatically validates the incoming 'user' data against UserCreate.
    Depends(get_db) securely opens and closes a database session for this specific request.
    """
    return user_service.create_user(db=db, user=user)