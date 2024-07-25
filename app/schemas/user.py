from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
  # email: str = Field(email=True)
  # username: str = Field(min_length=3, max_length=16)
  # first_name: str = Field(min_length=2, max_length=16)
  # last_name: str = Field(min_length=2, max_length=16)
  # hashed_password = 
  # is_active: bool = Field()
  # role
  username: str
  email: str
  first_name: str
  last_name: str
  password: str
  role: str