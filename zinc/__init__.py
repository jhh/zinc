from urllib.request import urlopen
from flask import Flask
from flask.templating import render_template

from zinc.status.status import Status


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from . import api
    app.register_blueprint(api.bp)

    from . import console
    app.register_blueprint(console.bp)

    return app
