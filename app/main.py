from fastapi import FastAPI
import models.todo as todo
from db.session import engine

app = FastAPI()

todo.Base.metadata.create_all(bind=engine)