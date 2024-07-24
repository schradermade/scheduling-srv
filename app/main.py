from fastapi import FastAPI
from models.todo import Base
from db.session import engine
from endpoints import todo

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(todo.router)
