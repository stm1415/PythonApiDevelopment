
# pytest -v -s tests\test_posts.py
from typing import List
from app import schemas
import pytest

def test_unauthorized_user_get_posts(client):
    response = client.get("/posts/")

    assert response.status_code == 401


def test_unathorized_user_get_single_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401

def test_unauthorized_user_get_single_post_not_found(client):
    response = client.get(f"/posts/200")

    assert response.status_code == 401

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")

    posts = response.json()

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, posts)
    posts_list = list(posts_map)

    assert response.status_code == 200
    assert len(posts) == len(test_posts)
    # assert posts_list[0].Post.title == test_posts[0].title

def test_get_single_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")

    post = response.json()
    post = schemas.PostOut(**post)
    assert response.status_code == 200
    assert post.Post.title == test_posts[0].title

def test_get_single_post_not_found(authorized_client):
    response = authorized_client.get(f"/posts/200")

    assert response.status_code == 404



@pytest.mark.parametrize("title, content, published, status_code", [
    ("HELLO 1", "This is world 1", True, 201),
    ("HELLO 2", "This is world 2", False, 201),
    ("HELLO 3", "This is world 3", True, 201),
])
def test_create_post(authorized_client,test_user, title, content, published, status_code):
    response = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "published": published}
    )

    post = response.json()
    post = schemas.Post(**post)

    assert response.status_code == status_code
    assert post.title == title
    assert post.content == content
    assert post.published == published
    assert post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client,test_user):
    response = authorized_client.post(
        "/posts/",
        json={"title": "HELLO 4", "content": "This is world 4"}
    )

    post = response.json()
    post = schemas.Post(**post)

    assert response.status_code == 201
    assert post.published == True
    assert post.owner_id == test_user['id']

def test_create_post_unauthorized_user(client):
    response = client.post(
        "/posts/",
        json={"title": "HELLO 1", "content": "This is world 1", "published": True}
    )

    assert response.status_code == 401




def test_delete_post_unauthorized_user(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 401

def test_delete_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert response.status_code == 204

def test_delete_post_not_found(authorized_client):
    response = authorized_client.delete(f"/posts/200")

    assert response.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert response.status_code == 403



def test_update_post_unauthorized_user(client, test_posts):
    response = client.put(
        f"/posts/{test_posts[0].id}",
        json={"title": "HELLO 1", "content": "This is world 1", "published": True}
    )

    assert response.status_code == 401

def test_update_post(authorized_client, test_posts):
    response = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json={"title": "HELLO 111", "content": "This is world 1111", "published": True}
    )

    post = response.json()
    post = schemas.Post(**post)

    assert response.status_code == 200
    assert post.title == "HELLO 111"
    assert post.content == "This is world 1111"
    assert post.published == True
    assert post.id == test_posts[0].id


def test_update_post_not_found(authorized_client):
    response = authorized_client.put(
        f"/posts/200",
        json={"title": "HELLO 1", "content": "This is world 1", "published": True}
    )

    assert response.status_code == 404

def test_update_other_user_post(authorized_client, test_posts):
    response = authorized_client.put(
        f"/posts/{test_posts[3].id}",
        json={"title": "HELLO 111", "content": "This is world 111", "published": True}
    )

    assert response.status_code == 403