from pydantic import BaseModel, Field
from datetime import datetime, timezone

class CreateBlog(BaseModel):
    title: str = Field(...,min_length = 5, max_length = 50, description = "Title of the blog must be between 5 to 50 characters")
    content: str = Field(..., min_length = 10, max_length = 5000, description = "Content of the blog must be between 10 to 5000 characters")

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    # created_at: int(datetime.now(timezone.utc).timestamp())
    author_id: str

    class Config:
        from_attributes = True

