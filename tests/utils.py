import os
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Todos, User
from app.routers.auth import bcrypt_context

from app.main import app
from app.db.session import Base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('TEST_DATABASE_URL')

engine = create_engine(
  SQLALCHEMY_DATABASE_URL,
  connect_args={'check_same_thread': False },
  poolclass = StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
  db = TestingSessionLocal()
  try:
    yield db
  finally:
    db.close()
    
def override_get_current_user():
  return { 'username': 'schradermade', 'id': 1, 'user_role': 'admin' }

client = TestClient(app)

@pytest.fixture
def test_todo():
  todo = Todos(
    title='Learn to code',
    description='Need to learn everyday',
    priority=5,
    complete=False,
    owner_id=1
  )
  
  db = TestingSessionLocal()
  db.add(todo)
  db.commit()
  yield todo
  with engine.connect() as connection:
    connection.execute(text('DELETE FROM todos;'))
    connection.commit()
    
@pytest.fixture
def test_user():
  user = User(
    email='test123@gmail.com',
    username='test_username1',
    first_name='test',
    last_name='user',
    hashed_password=bcrypt_context.hash('testpassword'),
    role='admin',
    is_active=True,
    phone_number='5555555555'
  )
  
  db = TestingSessionLocal()
  db.add(user)
  db.commit()
  yield user
  with engine.connect() as connection:
    connection.execute(text('DELETE FROM users;'))
    connection.commit()