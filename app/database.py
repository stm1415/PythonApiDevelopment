import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("No SQLALCHEMY_DATABASE_URL found in environment variables")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine ) # creates session objects used to interact with the database

Base = declarative_base() # define a database table

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()