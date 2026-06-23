from app.db.database import engine, Base
from app.db import models
from app.api import users
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")

# Register the router
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Blog App API"}
