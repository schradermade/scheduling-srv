from typing import Annotated
from fastapi import Depends, HTTPException
from starlette import status
from ..services.auth import get_current_user

user_dependency = Annotated[dict, Depends(get_current_user)]

def get_current_user(user: user_dependency):
  if user is None:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail='Authentication Failed'
    )
  return user