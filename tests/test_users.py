import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import schemas, models
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db

# pytest --disable-warnings
# pytest --disable-warnings -v -x --> to stop the test after the first failure

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:password123@localhost:5432/fastapi_test'
if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("No SQLALCHEMY_DATABASE_URL found in environment variables")
engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine ) # creates session objects used to interact with the database

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db  # override the get_db function used throughout the app

@pytest.fixture
def client():
    # run code before the test
    models.Base.metadata.drop_all(bind=engine) # drop the tables
    models.Base.metadata.create_all(bind=engine)  # create the tables
    yield TestClient(app)
    # run code after the test

def test_root(client):
    response = client.get("/")
    # print(response.json())
    # print(response.json()['message'])
    # print(response.json().get('message'))
    assert response.json()['message'] == "Welcome to my API course. This is the beginning of a new chapter. Hello world again dear"

    assert response.status_code == 200


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "hello13@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**response.json())  # use of pydantic model to validate the response
    assert response.status_code == 201
    assert new_user.email == "hello13@gmail.com"