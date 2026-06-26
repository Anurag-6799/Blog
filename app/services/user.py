from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext
from fastapi import HTTPException

# Set up the hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create the database model instance
    db_user = User(
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )

    db.add(db_user)      # Stage the transaction
    db.commit()          # Execute the transaction
    db.refresh(db_user)  # Fetch the newly generated ID from Supabase
    
    return db_user