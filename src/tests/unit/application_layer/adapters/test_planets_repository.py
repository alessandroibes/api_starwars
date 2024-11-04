import bson
import pytest

from starwars.app import mongo_client
from starwars.application_layer.adapters.planets_repository import PlanetsRepository
from starwars.domain_layer.ports.planets import DuplicatedPlanet, InvalidPlanet


def test_persist_planet(planet_info, client):
    planet_data = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": []
    }

    PlanetsRepository.persist_planet(**planet_data)

    inserted_planet = mongo_client.db.planets.find_one()
    assert inserted_planet["name"] == planet_info["name"]
    assert inserted_planet["climate"] == planet_info["climate"]
    assert inserted_planet["diameter"] == planet_info["diameter"]
    assert inserted_planet["population"] == planet_info["population"]


def test_persist_planet_must_raises_duplicated_planet_exception_when_planet_name_already_exists(planet_info, client):
    planet_data = {
        "name": planet_info["name"],
        "climate": "arid",
        "diameter": "10465",
        "population": "200000",
        "films": []
    }
    PlanetsRepository.persist_planet(**planet_data)

    with pytest.raises(
        DuplicatedPlanet, match=f"Planet with name {planet_info['name']} already exists"
    ):
        PlanetsRepository.persist_planet(
            name=planet_info["name"],
            climate="temperate",
            diameter="12500",
            population="2000000000",
            films=[]
        )


def test_persist_planet_must_raises_exception_when_one_or_more_films_do_not_exist(planet_info, client):
    planet_data = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": planet_info["films"]
    }

    with pytest.raises(
        Exception, match="One or more films do not exist"
    ):
        PlanetsRepository.persist_planet(**planet_data)


def test_update_planet(client):
    planet_data = {
        "name": "Planet1",
        "climate": "Climate1",
        "diameter": "Diameter1",
        "population": "Population1",
        "films": []
    }

    inserted_id = PlanetsRepository.persist_planet(**planet_data)
    inserted_planet = mongo_client.db.planets.find_one({"_id": bson.ObjectId(inserted_id)})

    assert inserted_planet["name"] == planet_data["name"]
    assert inserted_planet["climate"] == planet_data["climate"]
    assert inserted_planet["diameter"] == planet_data["diameter"]
    assert inserted_planet["population"] == planet_data["population"]

    updated_data = {
        "id": inserted_id,
        "name": "Planet2",
        "climate": "Climate2",
        "diameter": "Diameter2",
        "population": "Population2",
        "films": []
    }

    PlanetsRepository.update_planet(**updated_data)
    updated_planet = mongo_client.db.planets.find_one({"_id": bson.ObjectId(inserted_id)})

    assert updated_planet["name"] == updated_data["name"]
    assert updated_planet["climate"] == updated_data["climate"]
    assert updated_planet["diameter"] == updated_data["diameter"]
    assert updated_planet["population"] == updated_data["population"]


def test_update_planet_must_raises_duplicated_planet_exception_when_planet_name_already_exists(client):
    planet1_data = {
        "name": "Planet1",
        "climate": "Climate1",
        "diameter": "Diameter1",
        "population": "Population1",
        "films": []
    }

    PlanetsRepository.persist_planet(**planet1_data)

    planet2_data = {
        "name": "Planet2",
        "climate": "Climate2",
        "diameter": "Diameter2",
        "population": "Population2",
        "films": []
    }

    inserted_id2 = PlanetsRepository.persist_planet(**planet2_data)

    updated_data = {
        "id": inserted_id2,
        "name": "Planet1",
        "climate": "Climate2",
        "diameter": "Diameter2",
        "population": "Population2",
        "films": []
    }

    with pytest.raises(
        DuplicatedPlanet, match=f"Planet with name {updated_data['name']} already exists"
    ):
        PlanetsRepository.update_planet(**updated_data)


def test_update_planet_must_raises_exception_when_one_or_more_films_do_not_exist(planet_info, client):
    planet_data = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": []
    }

    inserted_id = PlanetsRepository.persist_planet(**planet_data)

    updated_data = {
        "id": inserted_id,
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": planet_info["films"]
    }

    with pytest.raises(
        Exception, match="One or more films do not exist"
    ):
        PlanetsRepository.update_planet(**updated_data)


def test_get_planet_by_id_must_return_inserted_planet(planet_info, client):
    planet_data = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": []
    }

    insterted_id = PlanetsRepository.persist_planet(**planet_data)

    inserted_planet = PlanetsRepository.get_planet_by_id(insterted_id)
    assert inserted_planet["name"] == planet_info["name"]
    assert inserted_planet["climate"] == planet_info["climate"]
    assert inserted_planet["diameter"] == planet_info["diameter"]
    assert inserted_planet["population"] == planet_info["population"]


def test_get_planet_must_raises_invalid_planet_exception_when_id_is_invalid():
    invalid_id = "123"

    with pytest.raises(
        InvalidPlanet, match=f"{invalid_id} is not a valid planet id."
    ):
        PlanetsRepository.get_planet_by_id(invalid_id)


def test_get_planet_must_return_none_when_planet_does_not_found(planet_info):
    inserted_planet = PlanetsRepository.get_planet_by_id(planet_info["id"])

    assert inserted_planet is None


def test_remove_planet(planet_info, client):
    planet_data = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": []
    }

    inserted_id = PlanetsRepository.persist_planet(**planet_data)
    removed_planet = PlanetsRepository.remove_planet(inserted_id)
    inserted_planet = mongo_client.db.planets.find_one({"_id": bson.ObjectId(inserted_id)})

    assert inserted_planet is None
    assert removed_planet is None
