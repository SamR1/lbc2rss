from flask import Flask


class TestConfig:
    def test_development_config(self, app: Flask) -> None:
        app.config.from_object('lbc2rss.config.DevelopmentConfig')
        assert app.config['DEBUG']
        assert not app.config['TESTING']

    def test_testing_config(self, app: Flask) -> None:
        app.config.from_object('lbc2rss.config.TestingConfig')
        assert app.config['DEBUG']
        assert app.config['TESTING']

    def test_prod_config(self, app: Flask) -> None:
        app.config.from_object('lbc2rss.config.ProductionConfig')
        assert not app.config['DEBUG']
        assert not app.config['TESTING']
