import os
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from starlette import status
from ..models import User
from ..utils.security import bcrypt_context, oauth2_bearer

load_dotenv()

SECRET_KEY = os.getenv('AUTH_SECRET_KEY')
ALGORITHM = 'HS256'

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({ 'exp': expires })
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials.'
        )