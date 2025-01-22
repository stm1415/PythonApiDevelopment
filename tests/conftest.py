# This file contains fixtures that are used in the tests. We dont need to use import statements in the test files to use these fixtures. The fixtures are automatically discovered by pytest and can be used in the test files.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app import models
from app.main import app
from fastapi.testclient import TestClient
from app.database import get_db
from app.oauth2 import create_access_token
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
@pytest.fixture(scope="function")  # @pytest.fixture
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


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello1415@gmail.com", "password": "password123"}

    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data['password']

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session):

    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }]

    def create_post_model(post):
        return models.Post(**post)
    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    #session.add_all([models.Post(**post) for post in posts_data])
    session.commit()

    return session.query(models.Post).all()
