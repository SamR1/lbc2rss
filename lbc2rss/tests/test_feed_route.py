from uuid import uuid4

from flask import Flask


class TestFeedRoute:
    def test_it_returns_feed_xml_version(self, app: Flask) -> None:
        client = app.test_client()
        response = client.get('/locations')
        assert response.status_code == 200
        data = response.data.decode()
        assert '<?xml version="1.0" encoding="UTF-8"?>' in data

    def test_it_raise_error_on_invalid_category(self, app: Flask) -> None:
        client = app.test_client()
        response = client.get(f'/{uuid4().hex}')
        assert response.status_code == 404
        data = response.data.decode()
        assert 'Invalid category.' in data
