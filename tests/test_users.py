import jwt
import pytest
from app import schemas
from app.config import settings

# pytest --disable-warnings
# pytest --disable-warnings -v -x --> to stop the test after the first failure
# pytest --disable-warnings -v -x tests/test_users.py --> to run a specific test file


def test_root(client):
    response = client.get("/")
    # print(response.json())
    # print(response.json()['message'])
    # print(response.json().get('message'))
    assert response.json()['message'] == "Hello world again dear. Successfully deployed from the github pipeline."

    assert response.status_code == 200


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"email": "hello13@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**response.json())  # use of pydantic model to validate the response
    assert response.status_code == 201
    assert new_user.email == "hello13@gmail.com"


def test_login_user(client, test_user):
    response = client.post(
        "/login",
        data={"username":test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.encryption_algorithm])
    id: int = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"

    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("hello1415@gmail.com", "wrongPasword", 403),
    ("wrongemail@gmail.com", "wrongPasword", 403),
    (None, None, 403),
    (None, "password123", 403),
    ("hello1415@gmail.com",None, 403),])
def test_incorrect_login(client, email, password, status_code):
    response = client.post(
        "/login",
        data={"username":email, "password": password})
    assert response.status_code == status_code
