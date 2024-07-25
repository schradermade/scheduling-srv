from fastapi import APIRouter, HTTPException, Path
from models.todo import Todos
from schemas.todo import TodoRequest
from starlette import status
from dependencies.db import db_dependancy

router = APIRouter()

@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(db: db_dependancy):
  return db.query(Todos).all()

@router.get('/{todo_id}', status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependancy, todo_id: int = Path(gt=0)):
  todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
  if todo_model is not None:
    return todo_model
  raise HTTPException(status_code=404, detail='Todo not found.')

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependancy, todo_request: TodoRequest):
  todo_model = Todos(**todo_request.model_dump())
  db.add(todo_model)
  db.commit()

@router.put('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependancy, 
                      todo_request: TodoRequest,
                      todo_id: int = Path(gt=0)):
  todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail='Todo not found')
  
  todo_model.title = todo_request.title
  todo_model.description = todo_request.description
  todo_model.priority = todo_request.priority
  todo_model.complete = todo_request.complete

  db.add(todo_model)
  db.commit()

@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependancy, todo_id: int = Path(gt=0)):
  todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
  if todo_model is None:
    raise HTTPException(status_code=404, detail='Todo not found')
  db.query(Todos).filter(Todos.id == todo_id).delete()
  db.commit()