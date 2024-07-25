from fastapi import FastAPI
from models.todo import Base
from db.session import engine
from routers.todo import router as TodoRouter
from routers.auth import router as AuthRouter  # Ensure the import path is correct

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(AuthRouter, prefix='/auth')
app.include_router(TodoRouter, prefix='/todo')