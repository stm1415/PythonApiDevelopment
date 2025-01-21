from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app import models
from app.main import app
from fastapi.testclient import TestClient
from app.database import get_db
import pytest

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:password123@localhost:5432/fastapi_test'
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("No SQLALCHEMY_DATABASE_URL found in environment variables")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine ) # creates session objects used to interact with the database

#@pytest.fixture(scope="module")  # scope module means that the fixture will run once per module
@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine) # drop the tables
    models.Base.metadata.create_all(bind=engine)  # create the tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


#@pytest.fixture(scope="module")
@pytest.fixture(scope="function")
def client(session):
    # run code before the test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db  # override the get_db function used throughout the app
    yield TestClient(app)
    # run code after the test