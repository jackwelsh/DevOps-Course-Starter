import os
from flask import Flask, current_app
from werkzeug.utils import import_string
import config


def create_app():

    # create and configure the app
    app = Flask(__name__)

    # load settings from the set config file
    app.config.from_object(config.Config())

    with app.app_context():

        # attach routes
        from .index.views import index
        app.register_blueprint(index)

        return app
