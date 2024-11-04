import flask_pymongo
import logging
import os
import sys

from flask import Flask
from flask_cors import CORS

ENV = os.environ.get("DEPLOY_ENV", "Development")


mongo_client = flask_pymongo.PyMongo()


def create_app(deploy_env: str = ENV) -> Flask:
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(f"starwars.config.{deploy_env}Config")

    __register_blueprints(app)
    __configure_logger(app)
    __register_commands(app)

    if app.testing:
        from mongomock import MongoClient

        mongo_client.cx = MongoClient()
        mongo_client.db = mongo_client.cx["api-startwars"]
    
    try:
        from uwsgidecorators import postfork
    except ImportError:
        # If not using uwsgi, init mongo client normally
        mongo_client.init_app(app)
    else:
        # If using uwsgi, init mongo client after forking app to each process, to avoid deadlocks
        @postfork
        def post_fork_init_db():
            mongo_client.init_app(app)

    return app


def __register_blueprints(app: Flask):
    from starwars.presentation_layer.views.index import bp_index
    from starwars.presentation_layer.views.films import bp_films
    from starwars.presentation_layer.views.planets import bp_planets

    app.register_blueprint(bp_index)
    app.register_blueprint(bp_films)
    app.register_blueprint(bp_planets)


def __configure_logger(app: Flask):
    logger = logging.getLogger("api-starwars")
    if not logger.hasHandlers():
        logger.setLevel(app.config["LOGS_LEVEL"])
        logger.addHandler(logging.StreamHandler(sys.stdout))


def __register_commands(app):
    from starwars.commands import configure_collections, drop_collections

    app.cli.command("drop-collections")(drop_collections)
    app.cli.command("configure-collections")(configure_collections)
