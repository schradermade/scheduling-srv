from fastapi import FastAPI
from .db.session import engine, Base
from .routers import TodoRouter, AuthRouter, AdminRouter, UserRouter

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get('/healthy')
def health_check():
  return { 'status': 'Healthy' }

app.include_router(AuthRouter)
app.include_router(TodoRouter)
app.include_router(AdminRouter)
app.include_router(UserRouter)