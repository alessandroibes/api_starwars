import bson
import logging

from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError
from typing import List

from starwars.app import mongo_client
from starwars.domain_layer.ports.films import (
    DuplicatedFilm,
    FilmsService,
    InvalidFilm
)

logger = logging.getLogger("api-starwars." + __name__)


class FilmsRepository(FilmsService):

    @classmethod
    def persist_film(
        cls,
        title: str,
        release_date: str,
        director: str,
        planets: List[str]
    ):
        logger.info(
            "Creating film",
            extra={
                "props": {
                    "service": "FilmsRepository",
                    "method": "persist_film",
                    "title": title
                }
            },
        )

        try:
            valid_planets = list(mongo_client.db.planets.find(
                {"_id": {"$in": [bson.ObjectId(planet_id) for planet_id in planets]}}
            ))

            if len(valid_planets) != len(planets):
                raise InvalidFilm("One or more planets do not exist")

            film = mongo_client.db.films.insert_one(
                {
                    "title": title,
                    "release_date": release_date,
                    "director": director,
                    "planets": planets,
                    "created": datetime.now(timezone.utc),
                    "edited": datetime.now(timezone.utc)
                }
            )

            return str(film.inserted_id)
        
        except DuplicateKeyError:
            raise DuplicatedFilm(f"Film with title {title} already exists")
        
        except Exception as e:
            logger.exception(
                "Error creating film",
                extra={
                    "props": {
                        "service": "FilmsRepository",
                        "method": "persist_film",
                        "title": title,
                        "error_message": str(e),
                    }
                },
            )

            raise e

    @classmethod
    def update_film(
        cls,
        id: str,
        title: str,
        release_date: str,
        director: str,
        planets: List[str]
    ):
        logger.info(
            "Updating film",
            extra={
                "props": {
                    "service": "FilmsRepository",
                    "method": "update_film",
                    "id": id,
                    "title": title
                }
            },
        )

        update_data = {
            "title": title,
            "release_date": release_date,
            "director": director,
            "planets": planets,
            "edited": datetime.now(timezone.utc)
        }

        try:
            valid_planets = list(mongo_client.db.planets.find(
                {"_id": {"$in": [bson.ObjectId(planet_id) for planet_id in planets]}}
            ))

            if len(valid_planets) != len(planets):
                raise InvalidFilm("One or more planets do not exist")

            mongo_client.db.films.update_one(
                {"_id": bson.ObjectId(id)}, {"$set": update_data}
            )
        
        except DuplicateKeyError:
            raise DuplicatedFilm(f"Film with title {title} already exists")

        except Exception as e:
            logger.exception(
                "Error updating film",
                extra={
                    "props": {
                        "service": "FilmsRepository",
                        "method": "update_film",
                        "id": id,
                        "title": title,
                        "error_message": str(e),
                    }
                },
            )

            raise e

    @classmethod
    def get_film_by_id(cls, id: str):
        logger.info(
            "Getting film",
            extra={
                "props": {
                    "service": "FilmsRepository",
                    "method": "get_film_by_id",
                    "id": id,
                }
            },
        )

        try:
            result = mongo_client.db.films.find_one({"_id": bson.ObjectId(id)})

        except bson.errors.InvalidId as e:
            logger.exception(
                "Invalid film Id",
                extra={
                    "props": {
                        "service": "FilmsRepository",
                        "method": "get_film_by_id",
                        "id": id,
                        "error_message": str(e),
                    }
                },
            )

            raise InvalidFilm(f"{id} is not a valid film id.")
        
        except Exception as e:
            logger.exception(
                "Error getting film",
                extra={
                    "props": {
                        "service": "FilmsRepository",
                        "method": "get_film_by_id",
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
    def remove_film(cls, id: str):
        logger.info(
            "Removing film",
            extra={
                "props": {
                    "service": "FilmsRepository",
                    "method": "remove_film",
                    "id": id
                }
            },
        )

        try:
            mongo_client.db.films.delete_one({"_id": bson.ObjectId(id)})

        except Exception as e:
            logger.exception(
                "Error removing film",
                extra={
                    "props": {
                        "service": "FilmsRepository",
                        "method": "remove_film",
                        "id": id,
                        "error_message": str(e),
                    }
                },
            )

            raise e
