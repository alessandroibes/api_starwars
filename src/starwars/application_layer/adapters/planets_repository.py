import bson
import logging

from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError
from typing import List

from starwars.app import mongo_client
from starwars.domain_layer.ports.planets import (
    DuplicatedPlanet,
    InvalidPlanet,
    PlanetsService
)

logger = logging.getLogger("api-starwars." + __name__)


class PlanetsRepository(PlanetsService):

    @classmethod
    def persist_planet(
        cls,
        name: str,
        climate: str,
        diameter: str,
        population: str,
        films: List[str]
    ):
        logger.info(
            "Creating planet",
            extra={
                "props": {
                    "service": "PlanetsRepository",
                    "method": "persist_planet",
                    "name": name
                }
            },
        )

        try:
            valid_films = list(mongo_client.db.films.find(
                {"_id": {"$in": [bson.ObjectId(film_id) for film_id in films]}}
            ))

            if len(valid_films) != len(films):
                raise InvalidPlanet("One or more films do not exist")

            planet = mongo_client.db.planets.insert_one(
                {
                    "name": name,
                    "climate": climate,
                    "diameter": diameter,
                    "population": population,
                    "films": films,
                    "created": datetime.now(timezone.utc),
                    "edited": datetime.now(timezone.utc)
                }
            )

            return str(planet.inserted_id)
        
        except DuplicateKeyError:
            raise DuplicatedPlanet(f"Planet with name {name} already exists")
        
        except Exception as e:
            logger.exception(
                "Error creating planet",
                extra={
                    "props": {
                        "service": "PlanetsRepository",
                        "method": "persist_planet",
                        "name": name,
                        "error_message": str(e),
                    }
                },
            )

            raise e

    @classmethod
    def update_planet(
        cls,
        id: str,
        name: str,
        climate: str,
        diameter: str,
        population: str,
        films: List[str]
    ):
        logger.info(
            "Updating planet",
            extra={
                "props": {
                    "service": "PlanetsRepository",
                    "method": "update_planet",
                    "id": id,
                    "name": name
                }
            },
        )

        update_data = {
            "name": name,
            "climate": climate,
            "diameter": diameter,
            "population": population,
            "films": films,
            "edited": datetime.now(timezone.utc)
        }

        try:
            valid_films = list(mongo_client.db.films.find(
                {"_id": {"$in": [bson.ObjectId(film_id) for film_id in films]}}
            ))

            if len(valid_films) != len(films):
                raise InvalidPlanet("One or more films do not exist")

            mongo_client.db.planets.update_one(
                {"_id": bson.ObjectId(id)}, {"$set": update_data}
            )

        except DuplicateKeyError:
            raise DuplicatedPlanet(f"Planet with name {name} already exists")

        except Exception as e:
            logger.exception(
                "Error updating planet",
                extra={
                    "props": {
                        "service": "PlanetsRepository",
                        "method": "update_planet",
                        "id": id,
                        "name": name,
                        "error_message": str(e),
                    }
                },
            )

            raise e
    
    @classmethod
    def get_planet_by_id(cls, id: str):
        logger.info(
            "Getting planet",
            extra={
                "props": {
                    "service": "PlanetsRepository",
                    "method": "get_planet_by_id",
                    "id": id,
                }
            },
        )

        try:
            result = mongo_client.db.planets.find_one({"_id": bson.ObjectId(id)})

        except bson.errors.InvalidId as e:
            logger.exception(
                "Invalid planet Id",
                extra={
                    "props": {
                        "service": "PlanetsRepository",
                        "method": "get_planet_by_id",
                        "id": id,
                        "error_message": str(e),
                    }
                },
            )

            raise InvalidPlanet(f"{id} is not a valid planet id.")
        
        except Exception as e:
            logger.exception(
                "Error getting planet",
                extra={
                    "props": {
                        "service": "PlanetsRepository",
                        "method": "get_planet_by_id",
                        "id": id,
                        "error_message": str(e),
                    }
                },
            )

            raise e
        
        if not result:
            return None

        cls._parse_id_field(result)

        return result
    
    @staticmethod
    def _parse_id_field(document: dict):
        document["id"] = str(document.pop("_id"))

    @classmethod
    def remove_planet(cls, id: str):
        logger.info(
            "Removing planet",
            extra={
                "props": {
                    "service": "PlanetsRepository",
                    "method": "remove_planet",
                    "id": id
                }
            },
        )

        try:
            mongo_client.db.planets.delete_one({"_id": bson.ObjectId(id)})

        except Exception as e:
            logger.exception(
                "Error removing planet",
                extra={
                    "props": {
                        "service": "PlanetsRepository",
                        "method": "remove_planet",
                        "id": id,
                        "error_message": str(e),
                    }
                },
            )

            raise e
