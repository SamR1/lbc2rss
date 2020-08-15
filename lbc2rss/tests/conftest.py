import os
from typing import Generator

import pytest
from lbc2rss import create_app

os.environ['FLASK_ENV'] = 'testing'
os.environ['APP_SETTINGS'] = 'lbc2rss.config.TestingConfig'


@pytest.fixture
def app() -> Generator:
    app = create_app()
    with app.app_context():
        yield app
    return app
