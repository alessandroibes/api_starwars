import bson
import pytest

from starwars.app import mongo_client
from starwars.application_layer.adapters.films_repository import FilmsRepository
from starwars.domain_layer.ports.films import DuplicatedFilm, InvalidFilm


def test_persist_film(film_info, client):
    film_data = {
        "title": film_info["title"],
        "release_date": film_info["release_date"],
        "director": film_info["director"],
        "planets": []
    }

    FilmsRepository.persist_film(**film_data)

    inserted_film = mongo_client.db.films.find_one()
    assert inserted_film["title"] == film_info["title"]
    assert inserted_film["release_date"] == film_info["release_date"]
    assert inserted_film["director"] == film_info["director"]


def test_persist_film_must_raises_duplicated_film_exception_when_film_title_already_exists(film_info, client):
    film_data = {
        "title": film_info["title"],
        "release_date": "1977-05-01",
        "director": "George Lucas",
        "planets": []
    }
    FilmsRepository.persist_film(**film_data)

    with pytest.raises(
        DuplicatedFilm, match=f"Film with title {film_info['title']} already exists"
    ):
        FilmsRepository.persist_film(
            title=film_info["title"],
            release_date="1977-05-05",
            director="Rian Johnson",
            planets=[]
        )


def test_persist_film_must_raises_exception_when_one_or_more_planets_do_not_exist(film_info, client):
    film_data = {
        "title": film_info["title"],
        "release_date": film_info["release_date"],
        "director": film_info["director"],
        "planets": film_info["planets"]
    }

    with pytest.raises(
        Exception, match="One or more planets do not exist"
    ):
        FilmsRepository.persist_film(**film_data)


def test_update_film(client):
    film_data = {
        "title": "Title 1",
        "release_date": "1977-05-01",
        "director": "Director 1",
        "planets": []
    }

    inserted_id = FilmsRepository.persist_film(**film_data)
    inserted_film = mongo_client.db.films.find_one({"_id": bson.ObjectId(inserted_id)})

    assert inserted_film["title"] == film_data["title"]
    assert inserted_film["release_date"] == film_data["release_date"]
    assert inserted_film["director"] == film_data["director"]

    updated_data = {
        "id": inserted_id,
        "title": "Title 2",
        "release_date": "1977-05-05",
        "director": "Director 2",
        "planets": []
    }

    FilmsRepository.update_film(**updated_data)
    updated_film = mongo_client.db.films.find_one({"_id": bson.ObjectId(inserted_id)})

    assert updated_film["title"] == updated_data["title"]
    assert updated_film["release_date"] == updated_data["release_date"]
    assert updated_film["director"] == updated_data["director"]


def test_update_film_must_raises_duplicated_film_exception_when_film_title_already_exists(client):
    film1_data = {
        "title": "Title 1",
        "release_date": "1977-05-01",
        "director": "Director 1",
        "planets": []
    }

    FilmsRepository.persist_film(**film1_data)

    film2_data = {
        "title": "Title 2",
        "release_date": "1977-05-05",
        "director": "Director 2",
        "planets": []
    }

    inserted_id2 = FilmsRepository.persist_film(**film2_data)

    updated_data = {
        "id": inserted_id2,
        "title": "Title 1",
        "release_date": "1977-05-01",
        "director": "Director 1",
        "planets": []
    }

    with pytest.raises(
        DuplicatedFilm, match=f"Film with title {updated_data['title']} already exists"
    ):
        FilmsRepository.update_film(**updated_data)


def test_update_film_must_raises_exception_when_one_or_more_planets_do_not_exist(film_info, client):
    film_data = {
        "title": film_info["title"],
        "release_date": film_info["release_date"],
        "director": film_info["director"],
        "planets": []
    }

    inserted_id = FilmsRepository.persist_film(**film_data)

    updated_data = {
        "id": inserted_id,
        "title": film_info["title"],
        "release_date": film_info["release_date"],
        "director": film_info["director"],
        "planets": film_info["planets"]
    }

    with pytest.raises(
        Exception, match="One or more planets do not exist"
    ):
        FilmsRepository.update_film(**updated_data)


def test_get_film_by_id_must_return_inserted_film(film_info, client):
    film_data = {
        "title": film_info["title"],
        "release_date": film_info["release_date"],
        "director": film_info["director"],
        "planets": []
    }

    insterted_id = FilmsRepository.persist_film(**film_data)

    inserted_film = FilmsRepository.get_film_by_id(insterted_id)
    assert inserted_film["title"] == film_info["title"]
    assert inserted_film["release_date"] == film_info["release_date"]
    assert inserted_film["director"] == film_info["director"]


def test_get_film_must_raises_invalid_film_exception_when_id_is_invalid():
    invalid_id = "123"

    with pytest.raises(
        InvalidFilm, match=f"{invalid_id} is not a valid film id."
    ):
        FilmsRepository.get_film_by_id(invalid_id)


def test_get_film_must_return_none_when_film_does_not_found(film_info):
    inserted_film = FilmsRepository.get_film_by_id(film_info["id"])

    assert inserted_film is None


def test_remove_film(film_info, client):
    film_data = {
        "title": film_info["title"],
        "release_date": film_info["release_date"],
        "director": film_info["director"],
        "planets": []
    }

    inserted_id = FilmsRepository.persist_film(**film_data)
    removed_film = FilmsRepository.remove_film(inserted_id)
    inserted_film = mongo_client.db.films.find_one({"_id": bson.ObjectId(inserted_id)})

    assert inserted_film is None
    assert removed_film is None
