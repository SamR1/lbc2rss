import logging
import os
from typing import Tuple

from flask import Flask
from lbc2rss.feed import generate_ads_feed
from lbc2rss.lbc import LBCQuery
from pylbc.exceptions import InvalidCategory

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

    @app.route('/<category>', methods=['GET'])
    def ads_feed(category: str) -> Tuple[str, int]:
        try:
            LBCQuery(category=category)
        except InvalidCategory:
            return 'Invalid category.', 404
        return generate_ads_feed(category), 200

    @app.route('/', methods=['GET'])
    def index_page() -> str:
        return 'Hello!'

    return app
