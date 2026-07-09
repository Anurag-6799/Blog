import jwt
import os 

from os import load_dotenv
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

secret_key = os.getenv('SECRET_KEY')
algorithm = os.getenv('ALGORITHM')
Access_token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")