import pytest

from datetime import datetime
from unittest import mock

from starwars.application_layer.adapters.planets_repository import PlanetsRepository
from starwars.application_layer.use_cases.planets import PlanetAlreadyRegistered, PlanetsUseCase
from starwars.domain_layer.models.planets import Planet
from starwars.domain_layer.ports.planets import DuplicatedPlanet
from starwars.presentation_layer.mappings import PlanetMapping


@mock.patch.object(Planet, "create_planet")
def test_create_planet(create_planet_mock, return_planet_data_response):
    create_planet_mock.return_value = Planet(
        id=return_planet_data_response.id,
        name=return_planet_data_response.name,
        climate=return_planet_data_response.climate,
        diameter=return_planet_data_response.diameter,
        population=return_planet_data_response.population,
        films=return_planet_data_response.films,
        created=datetime.now(),
        edited=datetime.now()
    )

    data = PlanetMapping(
        payload={
            "name": return_planet_data_response.name,
            "climate": return_planet_data_response.climate,
            "diameter": return_planet_data_response.diameter,
            "population": return_planet_data_response.population
        }
    )

    created_planet = PlanetsUseCase.create_planet(data=data)

    create_planet_mock.assert_called_once_with(
        name=data.name,
        climate=data.climate,
        diameter=data.diameter,
        population=data.population,
        films=data.films,
        using_service=PlanetsRepository
    )

    assert isinstance(created_planet, dict)


@mock.patch.object(Planet, "create_planet")
def test_create_planet_must_raise_planet_already_registered_exception_when_name_already_exists(
    create_planet_mock,
    return_planet_data_response
):
    create_planet_mock.side_effect = DuplicatedPlanet()

    data = PlanetMapping(
        payload={
            "name": return_planet_data_response.name,
            "climate": return_planet_data_response.climate,
            "diameter": return_planet_data_response.diameter,
            "population": return_planet_data_response.population
        }
    )


    with pytest.raises(
        PlanetAlreadyRegistered, match=f"Planet with name {return_planet_data_response.name} already exists"
    ):
        PlanetsUseCase.create_planet(data=data)


@mock.patch.object(Planet, "update_planet")
def test_update_planet(update_planet_mock, return_planet_data_response):
    update_planet_mock.return_value = Planet(
        id=return_planet_data_response.id,
        name=return_planet_data_response.name,
        climate=return_planet_data_response.climate,
        diameter=return_planet_data_response.diameter,
        population=return_planet_data_response.population,
        films=return_planet_data_response.films,
        created=datetime.now(),
        edited=datetime.now()
    )

    data = PlanetMapping(
        payload={
            "name": return_planet_data_response.name,
            "climate": return_planet_data_response.climate,
            "diameter": return_planet_data_response.diameter,
            "population": return_planet_data_response.population
        }
    )

    updated_planet = PlanetsUseCase.update_planet(
        id=return_planet_data_response.id,
        data=data
    )

    update_planet_mock.assert_called_once_with(
        id=return_planet_data_response.id,
        name=data.name,
        climate=data.climate,
        diameter=data.diameter,
        population=data.population,
        films=data.films,
        using_service=PlanetsRepository
    )

    assert isinstance(updated_planet, dict)


@mock.patch.object(Planet, "update_planet")
def test_update_planet_must_raise_planet_already_registered_exception_when_name_already_exists(
    update_planet_mock,
    return_planet_data_response
):
    update_planet_mock.side_effect = DuplicatedPlanet()

    data = PlanetMapping(
        payload={
            "name": return_planet_data_response.name,
            "climate": return_planet_data_response.climate,
            "diameter": return_planet_data_response.diameter,
            "population": return_planet_data_response.population
        }
    )

    with pytest.raises(
        PlanetAlreadyRegistered, match=f"Planet with name {return_planet_data_response.name} already exists"
    ):
        PlanetsUseCase.update_planet(
            id=return_planet_data_response.id,
            data=data
        )


@mock.patch.object(Planet, "remove_planet")
def test_remove_planet(remove_planet_mock):
    id = "123"
    removed_planet = PlanetsUseCase.remove_planet(id=id)

    remove_planet_mock.assert_called_once_with(
        id=id,
        using_service=PlanetsRepository
    )

    assert removed_planet is None


@mock.patch.object(Planet, "get_planet_by_id")
def test_get_planet_by_id(get_planet_by_id, return_planet_data_response):
    get_planet_by_id.return_value = Planet(
        id=return_planet_data_response.id,
        name=return_planet_data_response.name,
        climate=return_planet_data_response.climate,
        diameter=return_planet_data_response.diameter,
        population=return_planet_data_response.population,
        films=return_planet_data_response.films,
        created=datetime.now(),
        edited=datetime.now()
    )

    response = PlanetsUseCase.get_planet_by_id(id=return_planet_data_response.id)

    get_planet_by_id.assert_called_once_with(
        return_planet_data_response.id,
        using_service=PlanetsRepository
    )

    assert isinstance(response, dict)
