# source: http://docs.gunicorn.org/en/stable/custom.html
import multiprocessing
import os
from typing import Dict

import gunicorn.app.base
from flask import Flask
from lbc2rss import create_app


def number_of_workers() -> int:
    return (multiprocessing.cpu_count() * 2) + 1


if not os.getenv('APP_SETTINGS'):
    os.environ['APP_SETTINGS'] = 'lbc2rss.config.ProductionConfig'
HOST = os.getenv('APP_HOST', '0.0.0.0')
PORT = os.getenv('APP_PORT', '5000')
WORKERS = os.getenv('APP_WORKERS', number_of_workers())
BASEDIR = os.path.abspath(os.path.dirname(__file__))
app = create_app()


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, current_app: Flask, options: Dict = None) -> None:
        self.options = options or {}
        self.application = current_app
        super().__init__()

    def load_config(self) -> None:
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> Flask:
        return self.application


def main() -> None:
    options = {'bind': f'{HOST}:{PORT}', 'workers': WORKERS}
    StandaloneApplication(app, options).run()


if __name__ == '__main__':
    main()
