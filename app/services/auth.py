from passlib.context import CryptContext

# 1. Initialize the hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. Function to generate a new hash (used during User Registration)
def get_password_hash(password: str) -> str:
    """Takes a plain-text password and returns a secure bcrypt hash."""
    return pwd_context.hash(password)

# 3. Function to compare passwords (used during Login)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Hashes the plain_password and checks if it mathematically matches 
    the hashed_password pulled from the database.
    """
    return pwd_context.verify(plain_password, hashed_password)