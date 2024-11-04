from unittest import mock

from starwars.application_layer.use_cases.planets import PlanetAlreadyRegistered, PlanetsUseCase


PLANETS_RESOURCE = "/api/planets"


@mock.patch.object(PlanetsUseCase, "create_planet")
def test_post_planets_must_return_added_planet_and_201_when_success(create_planet_mock, planet_info, client):
    request_json = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": planet_info["films"]
    }

    create_planet_mock.return_value = planet_info

    response = client.post(PLANETS_RESOURCE, json=request_json)

    assert response.status_code == 201
    assert response.json == planet_info
    assert create_planet_mock.call_args.kwargs["data"].payload == request_json


@mock.patch.object(PlanetsUseCase, "create_planet")
def test_post_planets_must_return_409_when_planet_name_already_registered(create_planet_mock, planet_info, client):
    request_json = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": planet_info["films"]
    }

    error_message = f"Film with name {planet_info['name']} already exists"
    create_planet_mock.side_effect = PlanetAlreadyRegistered(error_message)

    response = client.post(PLANETS_RESOURCE, json=request_json)

    assert response.status_code == 409
    assert response.json == {"message": error_message}


@mock.patch.object(PlanetsUseCase, "create_planet")
def test_post_planets_must_return_400_when_create_planet_raises_an_generic_exception(create_planet_mock, planet_info, client):
    request_json = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": planet_info["films"]
    }

    error_message = "Generic error"
    create_planet_mock.side_effect = Exception(error_message)

    response = client.post(PLANETS_RESOURCE, json=request_json)

    assert response.status_code == 400
    assert response.json == {"message": error_message}


@mock.patch.object(PlanetsUseCase, "get_planet_by_id")
def test_get_planets_must_return_200_when_success(get_planet_by_id_mock, planet_info, client):
    get_planet_by_id_mock.return_value = planet_info

    response = client.get(PLANETS_RESOURCE + f"/{planet_info['id']}")

    assert response.status_code == 200
    assert response.json == planet_info
    assert get_planet_by_id_mock.call_args.kwargs["id"] == planet_info["id"]


@mock.patch.object(PlanetsUseCase, "get_planet_by_id")
def test_get_planets_must_return_400_when_get_planet_by_id_raises_and_generic_exception(get_planet_by_id_mock, client):
    error_message = "Generic error"
    get_planet_by_id_mock.side_effect = Exception(error_message)

    response = client.get(PLANETS_RESOURCE + "/123")

    assert response.status_code == 400
    assert response.json == {"message": error_message}


@mock.patch.object(PlanetsUseCase, "get_planet_by_id")
def test_get_planets_must_return_404_when_planet_not_found(get_planet_by_id_mock, client):
    get_planet_by_id_mock.return_value = None

    id = "123"
    response = client.get(PLANETS_RESOURCE + f"/{id}")

    assert response.status_code == 404
    assert response.json == {"message": f"Planet with id {id} was not found"}


@mock.patch.object(PlanetsUseCase, "update_planet")
def test_put_planets_must_return_updated_planet_and_200_when_success(update_planet_mock, planet_info, client):
    request_json = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": planet_info["films"]
    }

    update_planet_mock.return_value = planet_info

    response = client.put(PLANETS_RESOURCE + f"/{planet_info['id']}", json=request_json)

    assert response.status_code == 200
    assert response.json == planet_info
    assert update_planet_mock.call_args.kwargs["data"].payload == request_json


@mock.patch.object(PlanetsUseCase, "update_planet")
def test_put_planets_must_return_409_when_film_planet_already_registered(update_planet_mock, planet_info, client):
    request_json = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": planet_info["films"]
    }

    error_message = f"Planet with name {planet_info['name']} already exists"
    update_planet_mock.side_effect = PlanetAlreadyRegistered(error_message)

    response = client.put(PLANETS_RESOURCE + f"/{planet_info['id']}", json=request_json)

    assert response.status_code == 409
    assert response.json == {"message": error_message}


@mock.patch.object(PlanetsUseCase, "update_planet")
def test_put_planets_must_return_400_when_update_planet_raises_an_generic_exception(update_planet_mock, planet_info, client):
    request_json = {
        "name": planet_info["name"],
        "climate": planet_info["climate"],
        "diameter": planet_info["diameter"],
        "population": planet_info["population"],
        "films": planet_info["films"]
    }

    error_message = "Generic error"
    update_planet_mock.side_effect = Exception(error_message)

    response = client.put(PLANETS_RESOURCE + f"/{planet_info['id']}", json=request_json)

    assert response.status_code == 400
    assert response.json == {"message": error_message}


@mock.patch.object(PlanetsUseCase, "remove_planet")
def test_delete_planets_must_return_204_when_success(remove_planet_mock, client):
    remove_planet_mock.return_value = None

    response = client.delete(PLANETS_RESOURCE + "/123")

    assert response.status_code == 204


@mock.patch.object(PlanetsUseCase, "remove_planet")
def test_delete_planets_must_return_400_when_remove_planet_raises_an_generic_exception(remove_planet_mock, client):
    error_message = "Generic error"
    remove_planet_mock.side_effect = Exception(error_message)

    response = client.delete(PLANETS_RESOURCE + "/123")

    assert response.status_code == 400
    assert response.json == {"message": error_message}
