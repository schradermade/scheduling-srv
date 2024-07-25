from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from models.user import Users
from schemas.user import CreateUserRequest
from dependencies.db import db_dependancy
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import authenticate_user
from utils.security import bcrypt_context
from services.auth import create_access_token
from models.token import Token

router = APIRouter()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependancy,
                      create_user_request: CreateUserRequest):
    # create user model and assign the values from req body param
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )

    db.add(create_user_model)
    db.commit()

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: db_dependancy):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentication'
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return { 'access_token': token, 'token_type': 'bearer' }
