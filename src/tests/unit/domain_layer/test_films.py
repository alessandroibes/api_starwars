from starwars.domain_layer.models.films import Film


def test_create_film_must_call_persist_film_and_get_film_by_id_from_service_when_success(
    mocked_films_service,
    film_info
):
    Film.create_film(
        title=film_info["title"],
        release_date=film_info["release_date"],
        director=film_info["director"],
        planets=film_info["planets"],
        using_service=mocked_films_service
    )

    mocked_films_service.persist_film.assert_called_once_with(
        title=film_info["title"],
        release_date=film_info["release_date"],
        director=film_info["director"],
        planets=film_info["planets"]
    )

    mocked_films_service.get_film_by_id.assert_called_once_with(
        id=film_info["id"]
    )


def test_update_film_must_call_update_film_and_get_film_by_id_from_service_when_success(
    mocked_films_service,
    film_info
):
    Film.update_film(
        id=film_info["id"],
        title=film_info["title"],
        release_date=film_info["release_date"],
        director=film_info["director"],
        planets=film_info["planets"],
        using_service=mocked_films_service
    )

    mocked_films_service.update_film.assert_called_once_with(
        id=film_info["id"],
        title=film_info["title"],
        release_date=film_info["release_date"],
        director=film_info["director"],
        planets=film_info["planets"]
    )

    mocked_films_service.get_film_by_id.assert_called_once_with(
        id=film_info["id"]
    )


def test_get_film_must_return_object_when_receive_a_dict(
    film_info
):
    film = Film.get_film(film_info)

    assert film.id == film_info["id"]
    assert film.title == film_info["title"]
    assert film.release_date == film_info["release_date"]
    assert film.director == film_info["director"]
    assert film.planets == film_info["planets"]
    assert film.created == film_info["created"]
    assert film.edited == film_info["edited"]


def test_get_film_must_return_none_when_receive_a_empty_dict():
    film = Film.get_film({})

    assert film is None


def test_get_film_by_id_must_call_get_film_by_id_from_service_and_return_a_film_object(
    mocked_films_service,
    film_info
):
    film = Film.get_film_by_id(
        id=film_info["id"],
        using_service=mocked_films_service
    )

    mocked_films_service.get_film_by_id.assert_called_once_with(
        id=film_info["id"]
    )

    assert isinstance(film, Film)


def test_remove_film_must_call_remove_film_from_service(
    mocked_films_service,
    film_info
):
    Film.remove_film(
        id=film_info["id"],
        using_service=mocked_films_service
    )

    mocked_films_service.remove_film.assert_called_once_with(
        id=film_info["id"]
    )
