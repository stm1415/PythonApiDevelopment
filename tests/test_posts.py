
# pytest -v -s tests\test_posts.py
from typing import List
from app import schemas

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