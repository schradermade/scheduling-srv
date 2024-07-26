from fastapi import APIRouter, Depends, HTTPException
from models.user import Users
from starlette import status
from dependencies.db import db_dependency
from dependencies.dependencies import get_current_user
from utils.security import bcrypt_context
from models.user import UserVerification

router = APIRouter(
  prefix='/user',
  tags=['user']
)

@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency,
                   user: dict = Depends(get_current_user)):
  return db.query(Users).filter(Users.id == user.get('id')).first()

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(db: db_dependency,
                          user_verification: UserVerification,
                          user: dict = Depends(get_current_user)):
  user_model = db.query(Users).filter(Users.id == user.get('id')).first()

  if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
    raise HTTPException(status_code=401, detail='Error on password change')

  user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
  db.add(user_model)
  db.commit()