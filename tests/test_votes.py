from app import schemas

def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post(
        "/votes/",
        json={"post_id": test_posts[0].id, "dir": 1}
    )

    assert response.status_code == 201

def test_vote_on_post_twice(authorized_client, test_posts, test_votes):
    response = authorized_client.post(
        "/votes/",
        json={"post_id": test_posts[0].id, "dir": 1}
    )
    assert response.status_code == 409

def test_remove_vote(authorized_client, test_posts, test_votes):
    response = authorized_client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 0})

    assert response.status_code == 201

def test_remove_vote_not_voted(authorized_client, test_posts):
    response = authorized_client.post("/votes/", json={"post_id": test_posts[2].id, "dir": 0})

    assert response.status_code == 404

def test_vote_on_non_existent_post(authorized_client):
    response = authorized_client.post("/votes/", json={"post_id": 999, "dir": 1})

    assert response.status_code == 404

def test_vote_unathorized_user(client, test_posts):
    response = client.post("/votes/", json={"post_id": test_posts[0].id, "dir": 1})

    assert response.status_code == 401