import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.session import Base
from app.main import app
from app.dependencies.dependencies import get_current_user
from app.dependencies.db import get_db
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from app.models import Todos

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

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

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

def test_read_all_authenticated(test_todo):
  response = client.get('/todo/')
  assert response.status_code == status.HTTP_200_OK
  assert response.json() == [{'complete': False, 
                              'title': 'Learn to code', 
                              'description': 'Need to learn everyday', 
                              'id': 1, 
                              'priority': 5,
                              'owner_id': 1}]

def test_read_one_authenticated(test_todo):
  response = client.get('/todo/1')
  assert response.status_code == status.HTTP_200_OK
  assert response.json() == {'complete': False, 
                              'title': 'Learn to code', 
                              'description': 'Need to learn everyday', 
                              'id': 1, 
                              'priority': 5,
                              'owner_id': 1}

def test_read_one_authenticated_not_found():
  response = client.get('/todo/999')
  assert response.status_code == 404
  assert response.json() == { 'detail': 'Todo not found.' }