from .utils import *
from app.services.auth import authenticate_user
from app.dependencies.db import get_db

app.dependency_overrides[get_db] = override_get_db

def test_authenticate_user(test_user):
  db = TestingSessionLocal()
  authenticated_user = authenticate_user(test_user.username, 'testpassword', db)
  assert authenticated_user is not None
  assert authenticated_user.username == test_user.username
  
  non_existent_user = authenticate_user('wrongusername', 'testpassword', db)
  assert non_existent_user is False
  
  wrong_password_user = authenticate_user(test_user.username, 'wrongpassword', db)
  assert wrong_password_user is False