from unittest import mock

from starwars.application_layer.use_cases.films import FilmAlreadyRegistered, FilmsUseCase


FILMS_RESOURCE = "/api/films"


@mock.patch.object(FilmsUseCase, "create_film")
def test_post_films_must_return_added_film_and_201_when_success(create_film_mock, film_info, client):
    request_json = {
        "title": film_info["title"],
        "director": film_info["director"],
        "release_date": film_info["release_date"],
        "planets": film_info["planets"]
    }

    create_film_mock.return_value = film_info

    response = client.post(FILMS_RESOURCE, json=request_json)

    assert response.status_code == 201
    assert response.json == film_info
    assert create_film_mock.call_args.kwargs["data"].payload == request_json


@mock.patch.object(FilmsUseCase, "create_film")
def test_post_films_must_return_409_when_film_title_already_registered(create_film_mock, film_info, client):
    request_json = {
        "title": film_info["title"],
        "director": film_info["director"],
        "release_date": film_info["release_date"],
        "planets": film_info["planets"]
    }

    error_message = f"Film with title {film_info['title']} already exists"
    create_film_mock.side_effect = FilmAlreadyRegistered(error_message)

    response = client.post(FILMS_RESOURCE, json=request_json)

    assert response.status_code == 409
    assert response.json == {"message": error_message}


@mock.patch.object(FilmsUseCase, "create_film")
def test_post_films_must_return_400_when_create_film_raises_an_generic_exception(create_film_mock, film_info, client):
    request_json = {
        "title": film_info["title"],
        "director": film_info["director"],
        "release_date": film_info["release_date"],
        "planets": film_info["planets"]
    }

    error_message = "Generic error"
    create_film_mock.side_effect = Exception(error_message)

    response = client.post(FILMS_RESOURCE, json=request_json)

    assert response.status_code == 400
    assert response.json == {"message": error_message}


@mock.patch.object(FilmsUseCase, "get_film_by_id")
def test_get_films_must_return_200_when_success(get_film_by_id_mock, film_info, client):
    get_film_by_id_mock.return_value = film_info

    response = client.get(FILMS_RESOURCE + f"/{film_info['id']}")

    assert response.status_code == 200
    assert response.json == film_info
    assert get_film_by_id_mock.call_args.kwargs["id"] == film_info["id"]


@mock.patch.object(FilmsUseCase, "get_film_by_id")
def test_get_films_must_return_400_when_get_film_by_id_raises_and_generic_exception(get_film_by_id_mock, client):
    error_message = "Generic error"
    get_film_by_id_mock.side_effect = Exception(error_message)

    response = client.get(FILMS_RESOURCE + "/123")

    assert response.status_code == 400
    assert response.json == {"message": error_message}


@mock.patch.object(FilmsUseCase, "get_film_by_id")
def test_get_films_must_return_404_when_film_not_found(get_film_by_id_mock, client):
    get_film_by_id_mock.return_value = None

    id = "123"
    response = client.get(FILMS_RESOURCE + f"/{id}")

    assert response.status_code == 404
    assert response.json == {"message": f"Film with id {id} was not found"}


@mock.patch.object(FilmsUseCase, "update_film")
def test_put_films_must_return_updated_film_and_200_when_success(update_film_mock, film_info, client):
    request_json = {
        "title": film_info["title"],
        "director": film_info["director"],
        "release_date": film_info["release_date"],
        "planets": film_info["planets"]
    }

    update_film_mock.return_value = film_info

    response = client.put(FILMS_RESOURCE + f"/{film_info['id']}", json=request_json)

    assert response.status_code == 200
    assert response.json == film_info
    assert update_film_mock.call_args.kwargs["data"].payload == request_json


@mock.patch.object(FilmsUseCase, "update_film")
def test_put_films_must_return_409_when_film_title_already_registered(update_film_mock, film_info, client):
    request_json = {
        "title": film_info["title"],
        "director": film_info["director"],
        "release_date": film_info["release_date"],
        "planets": film_info["planets"]
    }

    error_message = f"Film with title {film_info['title']} already exists"
    update_film_mock.side_effect = FilmAlreadyRegistered(error_message)

    response = client.put(FILMS_RESOURCE + f"/{film_info['id']}", json=request_json)

    assert response.status_code == 409
    assert response.json == {"message": error_message}


@mock.patch.object(FilmsUseCase, "update_film")
def test_put_films_must_return_400_when_update_film_raises_an_generic_exception(update_film_mock, film_info, client):
    request_json = {
        "title": film_info["title"],
        "director": film_info["director"],
        "release_date": film_info["release_date"],
        "planets": film_info["planets"]
    }

    error_message = "Generic error"
    update_film_mock.side_effect = Exception(error_message)

    response = client.put(FILMS_RESOURCE + f"/{film_info['id']}", json=request_json)

    assert response.status_code == 400
    assert response.json == {"message": error_message}


@mock.patch.object(FilmsUseCase, "remove_film")
def test_delete_films_must_return_204_when_success(remove_film_mock, client):
    remove_film_mock.return_value = None

    response = client.delete(FILMS_RESOURCE + "/123")

    assert response.status_code == 204


@mock.patch.object(FilmsUseCase, "remove_film")
def test_delete_films_must_return_400_when_remove_film_raises_an_generic_exception(remove_film_mock, client):
    error_message = "Generic error"
    remove_film_mock.side_effect = Exception(error_message)

    response = client.delete(FILMS_RESOURCE + "/123")

    assert response.status_code == 400
    assert response.json == {"message": error_message}
