from unittest.mock import patch
from uuid import uuid4

from flask import Flask


class TestFeedRoute:
    @patch('lbc2rss.lbc.LBCQuery.get_results', lambda x: [])
    def test_it_returns_feed_xml_version(self, app: Flask) -> None:
        client = app.test_client()
        response = client.get('/locations?cities=Lyon,69000')
        assert response.status_code == 200
        data = response.data.decode()
        assert '<?xml version="1.0" encoding="UTF-8"?>' in data

    def test_it_returns_error_on_invalid_category(self, app: Flask) -> None:
        client = app.test_client()
        response = client.get(f'/{uuid4().hex}')
        assert response.status_code == 404
        data = response.data.decode()
        assert 'Invalid category.' in data

    def test_it_returns_error_on_invalid_query_parameters(
        self, app: Flask
    ) -> None:
        client = app.test_client()
        response = client.get(f'/locations?cities={uuid4().hex}')
        assert response.status_code == 400
        data = response.data.decode()
        assert (
            'A city must contain a name and a valid zip code (5 digits), '
            'separated with a comma.'
        ) in data

    def test_it_returns_error_query_parameters_are_missing(
        self, app: Flask
    ) -> None:
        client = app.test_client()
        response = client.get('/locations')
        assert response.status_code == 400
        data = response.data.decode()
        assert 'No parameters provided.' in data
