import logging
import os

from flask import Flask
from lbc2rss.feed import generate_ads_feed

log_file = os.getenv('APP_LOG')
logging.basicConfig(
    filename=log_file,
    format='%(asctime)s - %(name)s - %(levelname)s - ' '%(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
)
app_log = logging.getLogger('lbc2rss')


def create_app() -> Flask:
    app = Flask(__name__)
    app_log.setLevel(logging.DEBUG if app.debug else logging.INFO)

    @app.route('/<category>')
    def ads_feed(category: str) -> str:
        return generate_ads_feed(category)

    @app.route('/')
    def index_page() -> str:
        return 'Hello!'

    return app
