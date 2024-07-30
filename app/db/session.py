import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

# used to set up the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# function is used to create new sessions that will be used to interact with the database.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# function is used to create a base class that your database models will inherit from, 
# making it easy to define tables and columns in the database.
Base = declarative_base()
