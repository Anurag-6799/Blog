import jwt
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


# PASSWORD
# Initialize the hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Function to generate a new hash (used during User Registration)
def get_password_hash(password: str) -> str:
    """Takes a plain-text password and returns a secure bcrypt hash."""
    return pwd_context.hash(password)

# Function to compare passwords (used during Login)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Hashes the plain_password and checks if it mathematically matches 
    the hashed_password pulled from the database.
    """
    return pwd_context.verify(plain_password, hashed_password)


# TOKEN
def create_access_token(data: dict) -> str:
    """Takes a dictionary of user data and encodes it into a JWT."""
    to_encode = data.copy()
    
    # Calculate the expiration time (current UTC time + X minutes)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Sign the token using the secret key and the HS256 algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Intercepts the request, decodes the JWT, and returns the authenticated User.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decode the token (This will automatically fail if the token is expired or tampered with)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 2. Extract the user_id (stored under the 'sub' claim)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except jwt.PyJWTError:
        raise credentials_exception

    # 3. Verify the user actually still exists in our database
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise credentials_exception
        
    return user

