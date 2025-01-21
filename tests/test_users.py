from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    # print(response.json())
    # print(response.json()['message'])
    # print(response.json().get('message'))
    assert response.json()['message'] == "Welcome to my API course. This is the beginning of a new chapter. Hello world again dear"
