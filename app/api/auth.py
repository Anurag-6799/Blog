from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.services.auth import verify_password, generate_token


router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(form_data: Oauth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==form_data.user_name).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_token = generate_token(data={'sub': str(user.user_id)})
    return {"access_token": user_token, "token_type": "bearer"}

    