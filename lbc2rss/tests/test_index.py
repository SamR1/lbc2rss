from flask import Flask


def test_index_route(app: Flask) -> None:
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
    assert 'Hello!' in response.data.decode()
