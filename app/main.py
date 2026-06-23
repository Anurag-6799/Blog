from fastapi import FastAPI

app = FastAPI(title="Blog App")

@app.get("/")
def root():
    return {"message": "Welcome to the Blog App API"}
