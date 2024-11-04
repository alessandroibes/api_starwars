import pytest

from datetime import datetime
from unittest import mock

from starwars.application_layer.adapters.films_repository import FilmsRepository
from starwars.application_layer.use_cases.films import FilmAlreadyRegistered, FilmsUseCase
from starwars.domain_layer.models.films import Film
from starwars.domain_layer.ports.films import DuplicatedFilm
from starwars.presentation_layer.mappings import FilmMapping


@mock.patch.object(Film, "create_film")
def test_create_film(create_film_mock, return_film_data_response):
    create_film_mock.return_value = Film(
        id=return_film_data_response.id,
        title=return_film_data_response.title,
        release_date=return_film_data_response.release_date,
        director=return_film_data_response.director,
        planets=return_film_data_response.planets,
        created=datetime.now(),
        edited=datetime.now()
    )

    data = FilmMapping(
        payload={
            "title": return_film_data_response.title,
            "release_date": return_film_data_response.release_date,
            "director": return_film_data_response.director
        }
    )

    created_film = FilmsUseCase.create_film(data=data)

    create_film_mock.assert_called_once_with(
        title=data.title,
        release_date=data.release_date,
        director=data.director,
        planets=data.planets,
        using_service=FilmsRepository
    )

    assert isinstance(created_film, dict)


@mock.patch.object(Film, "create_film")
def test_create_film_must_raise_film_already_registered_exception_when_title_already_exists(
    create_film_mock,
    return_film_data_response
):
    create_film_mock.side_effect = DuplicatedFilm()

    data = FilmMapping(
        payload={
            "title": return_film_data_response.title,
            "release_date": return_film_data_response.release_date,
            "director": return_film_data_response.director
        }
    )


    with pytest.raises(
        FilmAlreadyRegistered, match=f"Film with title {return_film_data_response.title} already exists"
    ):
        FilmsUseCase.create_film(data=data)


@mock.patch.object(Film, "update_film")
def test_update_film(update_film_mock, return_film_data_response):
    update_film_mock.return_value = Film(
        id=return_film_data_response.id,
        title=return_film_data_response.title,
        release_date=return_film_data_response.release_date,
        director=return_film_data_response.director,
        planets=return_film_data_response.planets,
        created=datetime.now(),
        edited=datetime.now()
    )

    data = FilmMapping(
        payload={
            "title": return_film_data_response.title,
            "release_date": return_film_data_response.release_date,
            "director": return_film_data_response.director
        }
    )

    updated_film = FilmsUseCase.update_film(
        id=return_film_data_response.id,
        data=data
    )

    update_film_mock.assert_called_once_with(
        id=return_film_data_response.id,
        title=data.title,
        release_date=data.release_date,
        director=data.director,
        planets=data.planets,
        using_service=FilmsRepository
    )

    assert isinstance(updated_film, dict)


@mock.patch.object(Film, "update_film")
def test_update_film_must_raise_film_already_registered_exception_when_title_already_exists(
    update_film_mock,
    return_film_data_response
):
    update_film_mock.side_effect = DuplicatedFilm()

    data = FilmMapping(
        payload={
            "title": return_film_data_response.title,
            "release_date": return_film_data_response.release_date,
            "director": return_film_data_response.director
        }
    )

    with pytest.raises(
        FilmAlreadyRegistered, match=f"Film with title {return_film_data_response.title} already exists"
    ):
        FilmsUseCase.update_film(
            id=return_film_data_response.id,
            data=data
        )


@mock.patch.object(Film, "remove_film")
def test_remove_film(remove_film_mock):
    id = "123"
    removed_film = FilmsUseCase.remove_film(id=id)

    remove_film_mock.assert_called_once_with(
        id=id,
        using_service=FilmsRepository
    )

    assert removed_film is None


@mock.patch.object(Film, "get_film_by_id")
def test_get_film_by_id(get_film_by_id_mock, return_film_data_response):
    get_film_by_id_mock.return_value = Film(
        id=return_film_data_response.id,
        title=return_film_data_response.title,
        release_date=return_film_data_response.release_date,
        director=return_film_data_response.director,
        planets=return_film_data_response.planets,
        created=datetime.now(),
        edited=datetime.now()
    )

    response = FilmsUseCase.get_film_by_id(id=return_film_data_response.id)

    get_film_by_id_mock.assert_called_once_with(
        return_film_data_response.id,
        using_service=FilmsRepository
    )

    assert isinstance(response, dict)
