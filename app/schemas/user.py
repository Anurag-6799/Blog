from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    user_name: str = Field(...,min_length = 3, max_length=15, description="Username must be between 3 to 15 characters")
    email: EmailStr = Field(..., description="User's email")
    password: str = Field(...,min_length = 6, max_length=12, description="Password must be between 6 to 12 characters")

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        # This is magic: It tells Pydantic to read data directly from our SQLAlchemy database model
        from_attributes = True
    