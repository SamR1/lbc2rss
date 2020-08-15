from flask import Flask


class TestFeedRoute:
    def test_feed_route(self, app: Flask) -> None:
        client = app.test_client()
        response = client.get('/locations')
        assert response.status_code == 200
        data = response.data.decode()
        assert '<?xml version="1.0" encoding="UTF-8"?>' in data
        assert 'Recherche des offres "locations" sur Leboncoin' in data
