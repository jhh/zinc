from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    from . import api

    app.register_blueprint(api.bp)

    return app
