from datetime import timedata, datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestFormuth
from jose import jwt
from dotenv import load_dotenv
import os
from ..models.models import User
from ..deps import db_dependency, bycrypt_context

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
ALGORITHM = os.getenv('AUTH_ALGORITHM')

class UserCreateRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return False
    
    if not bycrypt_context.verify(password, user.hashed_password):
        return False
    
    return User

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = { 'sub': username, 'id': user_id }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({ 'exp': expires })
    return jwt.encode(encode, SECRET_KEY, algorith=ALGORITHM)

# @router.post('/', status_code=status.HTTP_201_CREATED)
# async def create_user(db: db_dependency, create_user_request: UserCreateRequest):
#     createuser_mmodel = User(
#         username=create_user_request.username
#         hashed_password=bycrypt_context.hash
#     )