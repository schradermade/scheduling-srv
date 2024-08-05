from fastapi import APIRouter, HTTPException, Path, Depends
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from ..models import Todos
from ..dependencies.dependencies import get_current_user
from ..db.session import SessionLocal

router = APIRouter(
  prefix='/admin',
  tags=['admin']
)

def get_db():
  db = SessionLocal()
  try:
    # yield means only the code prior to AND including the yield statement
    # is executed before sending a response.
    yield db
    # this code after the yield is executed after the response has been delivered
  finally:
    db.close()
    
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/todo', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
  if user is None or user.get('user_role') != 'admin':
    raise HTTPException(status_code=401, detail='Authentication Failed')
  return db.query(Todos).all()

@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
  if user is None or user.get('user_role') != 'admin':
    raise HTTPException(status_code=401, detail='Authentication Failed')
  todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail='Todo not found')
  db.query(Todos).filter(Todos.id == todo_id).delete()
  db.commit()