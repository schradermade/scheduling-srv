from fastapi import FastAPI
from models.todo import Base
from db.session import engine
from routers.todo import router as TodoRouter
from routers.auth import router as AuthRouter
from routers.admin import router as AdminRouter
from routers.users import router as UserRouter
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(AuthRouter)
app.include_router(TodoRouter)
app.include_router(AdminRouter)
app.include_router(UserRouter)