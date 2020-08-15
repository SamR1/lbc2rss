import logging
import os
from typing import Tuple

from flask import Flask, request
from lbc2rss.exceptions import InvalidParameters
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
            query = LBCQuery(category=category)
        except InvalidCategory:
            return 'Invalid category.', 404

        try:
            params = dict(request.args.copy())
            query.add_search_parameters(params)
        except InvalidParameters as error_message:
            return str(error_message), 400

        results = query.get_results()
        return generate_ads_feed(category, results, params), 200

    @app.route('/', methods=['GET'])
    def index_page() -> str:
        return 'Hello!'

    return app
