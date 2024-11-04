import logging

from flask import current_app
from flask.cli import with_appcontext

logger = logging.getLogger("api-starwars." + __name__)


class InvalidEnvironment(Exception):
    pass


def _configure_collections():
    from pymongo.errors import CollectionInvalid

    from starwars.app import mongo_client
    from starwars.application_layer.persistency.collections import (
        collections_definitions
    )

    for definition in collections_definitions:
        try:
            logger.info(f"Creating collection {definition.name}")

            collection = mongo_client.db.create_collection(
                name=definition.name, validator={"$jsonSchema": definition.validator}
            )
        except CollectionInvalid:
            logger.info(
                f"Collection {definition.name} already created, adding validator"
            )

            mongo_client.db.command(
                "collMod",
                definition.name,
                validator={"$jsonSchema": definition.validator},
            )
            collection = mongo_client.db.get_collection(definition.name)
        except Exception as e:
            logger.exception(
                f"Error creating collection {definition.name}. {type(e).__name__}: {e}"
            )
            raise e
        
        try:
            logger.info(f"Creating index on collection {definition.name}")

            collection.create_index(definition.index, unique=definition.unique_index)
        except Exception as e:
            logger.exception(
                f"Error creating index on collection {definition.name}. {type(e).__name__}: {e}"
            )
            raise e


def _drop_collections():
    from starwars.app import mongo_client

    collections = mongo_client.db.list_collection_names(
        filter={"name": {"$regex": r"^(?!system\.)"}}
    )

    for collection in collections:
        try:
            logger.info(f"Dropping collection {collection}")

            mongo_client.db.drop_collection(collection)
        except Exception as e:
            logger.exception(
                f"Error dropping collection {collection}. {type(e).__name__}: {e}"
            )
            raise e


@with_appcontext
def drop_collections():
    if current_app.config["DEPLOY_ENV"] == "Production":
        raise InvalidEnvironment("Drop/Create tables unable for production")
    _drop_collections()


@with_appcontext
def configure_collections():
    _configure_collections()