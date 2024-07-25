from db.session import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean

# ORM Models
class Todos(Base):
  __tablename__='todos'

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  description = Column(String)
  priority = Column(Integer)
  complete = Column(Boolean, default=False)
  owner_id = Column(Integer, ForeignKey('users.id'))