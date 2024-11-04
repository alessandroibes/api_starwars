from datetime import date
from typing import List
from unittest import mock

import pytest

from starwars.domain_layer.models.films import Film
from starwars.domain_layer.models.planets import Planet


@pytest.fixture(scope="function")
def client():
    from starwars.app import create_app, mongo_client

    def _load_collections_and_indexes():
        from starwars.application_layer.persistency.collections import (
            collections_definitions
        )

        for definition in collections_definitions:
            collection = mongo_client.db.create_collection(name=definition.name)
            collection.create_index(definition.index, unique=definition.unique_index)

    app = create_app("Testing")
    app.config["TESTING"] = True
    client = app.test_client()

    from mongomock import MongoClient
    mongo_client.cx = MongoClient()
    mongo_client.db = mongo_client.cx["api-clients"]

    _load_collections_and_indexes()

    with app.app_context():
        yield client


@pytest.fixture()
def fake_films_service_class(film_info):
    from starwars.domain_layer.ports.films import FilmsService

    class FakeFilmsService(FilmsService):
        @classmethod
        def persist_film(
            cls,
            title: str,
            release_date: str,
            director: str,
            planets: List[str]
        ):
            if title == film_info["title"]:
                return film_info["id"]
        
        @classmethod
        def update_film(
            cls,
            id: str,
            title: str,
            release_date: str,
            director: str,
            planets: List[str]
        ):
            return None
        
        @classmethod
        def get_film_by_id(cls, id: str):
            if id == film_info["id"]:
                return film_info
        
        @classmethod
        def remove_film(cls, id: str):
            return None
        
    return FakeFilmsService


@pytest.fixture()
def fake_planets_service_class(planet_info):
    from starwars.domain_layer.ports.planets import PlanetsService

    class FakePlanetsService(PlanetsService):
        @classmethod
        def persist_planet(
            cls,
            name: str,
            climate: str,
            diameter: str,
            population: str,
            films: List[str]
        ):
            if name == planet_info["name"]:
                return planet_info["id"]
        
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
            return None

        @classmethod
        def get_planet_by_id(cls, id: str):
            if id == planet_info["id"]:
                return planet_info
        
        @classmethod
        def remove_planet(cls, id: str):
            return None

    return FakePlanetsService


@pytest.fixture()
def mocked_films_service(fake_films_service_class):
    return mock.Mock(wraps=fake_films_service_class)


@pytest.fixture()
def mocked_planets_service(fake_planets_service_class):
    return mock.Mock(wraps=fake_planets_service_class)


@pytest.fixture()
def film_info():
    return {
        "id": "6726b6b6ecec0bd07cb1fef5",
        "title": "A New Hope",
        "release_date": "1977-05-25",
        "director": "George Lucas",
        "planets": [
            "6726b6e43f76b827df27c3cc",
            "6726b6eda679588fcebf3dbe",
            "6726b6f6d9b3080ad07b465a"
        ],
        "created": "2024-11-03T11:46:03.045+00:00",
        "edited": "2024-11-03T11:46:03.045+00:00"
    }


@pytest.fixture()
def planet_info():
    return {
        "id": "6727627bb5d077fbd23c3c59",
        "name": "Tatooine",
        "climate": "arid",
        "diameter": "10465",
        "population": "200000",
        "films": [
            "672762934817e2b2eac0d71d",
            "67276297257314d266a68175",
            "672762a0875fea2f97a2a9ce"
        ],
        "created": "2024-11-03T11:46:03.045+00:00",
        "edited": "2024-11-03T11:46:03.045+00:00"
    }


@pytest.fixture
def return_film_data_response(film_info):
    return Film(
        id=film_info["id"],
        title=film_info["title"],
        release_date=film_info["release_date"],
        director=film_info["director"],
        planets=film_info["planets"],
        created=film_info["created"],
        edited=film_info["edited"]
    )


@pytest.fixture
def return_planet_data_response(planet_info):
    return Planet(
        id=planet_info["id"],
        name=planet_info["name"],
        climate=planet_info["climate"],
        diameter=planet_info["diameter"],
        population=planet_info["population"],
        films=planet_info["films"],
        created=planet_info["created"],
        edited=planet_info["edited"]
    )
