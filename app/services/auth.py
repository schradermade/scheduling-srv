from datetime import timedelta, datetime, timezone
from sqlalchemy.orm import Session
from models.user import Users
from utils.security import bcrypt_context
from jose import jwt

SECRET_KEY = 'dc54fd359bd9ac6cc0cc262f4e6268e7f671ed988b447c72543f5d16c539de74'
ALGORITHM = 'HS256'

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({ 'exp': expires })
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)