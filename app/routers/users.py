from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from starlette import status
from ..models import User, UserVerification
from ..dependencies.dependencies import get_current_user
from ..dependencies.db import get_db
from ..utils.security import bcrypt_context
from passlib.context import CryptContext

router = APIRouter(
  prefix='/user',
  tags=['user']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency,
                   user: dict = Depends(get_current_user)):
  return db.query(User).filter(User.id == user.get('id')).first()

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db: db_dependency,
                          user_verification: UserVerification,
                          user: dict = Depends(get_current_user)):
  user_model = db.query(User).filter(User.id == user.get('id')).first()

  if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
    raise HTTPException(status_code=401, detail='Error on password change')

  user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
  db.add(user_model)
  db.commit()

@router.put('/phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(phone_number: str, db:db_dependency, user: dict = Depends(get_current_user)):
  # if user is None:
  #   raise HTTPException(status_code=401, deatil='Authentication Failed')
  user_model = db.query(User).filter(User.id == user.get('id')).first()
  user_model.phone_number = phone_number
  db.add(user_model)
  db.commit()