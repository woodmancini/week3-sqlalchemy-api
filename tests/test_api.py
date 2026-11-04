def test_starts_empty(client):
    response = client.get("/courses")
    assert response.status_code == 200
    assert response.json() == []