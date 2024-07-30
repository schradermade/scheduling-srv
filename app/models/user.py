from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean
from ..db.session import Base

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, unique=True)
  username = Column(String, unique=True)
  first_name = Column(String)
  last_name = Column(String)
  hashed_password = Column(String)
  is_active = Column(Boolean, default=True)
  role = Column(String)
  phone_number = Column(String)

class UserVerification(BaseModel):
  password: str
  new_password: str = Field(min_length=6)