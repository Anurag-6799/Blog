import jwt
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


# PASSWORD
# Initialize the hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
