
from app import schemas
from tests.database_test import client, session

# pytest --disable-warnings
# pytest --disable-warnings -v -x --> to stop the test after the first failure



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