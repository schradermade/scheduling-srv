from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from ..db.session import SessionLocal

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