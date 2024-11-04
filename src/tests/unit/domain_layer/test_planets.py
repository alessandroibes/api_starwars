from starwars.domain_layer.models.planets import Planet


def test_create_planet_must_call_persist_planet_and_get_planet_by_id_from_service_when_success(
    mocked_planets_service,
    planet_info
):
    Planet.create_planet(
        name=planet_info["name"],
        climate=planet_info["climate"],
        diameter=planet_info["diameter"],
        population=planet_info["population"],
        films=planet_info["films"],
        using_service=mocked_planets_service
    )

    mocked_planets_service.persist_planet.assert_called_once_with(
        name=planet_info["name"],
        climate=planet_info["climate"],
        diameter=planet_info["diameter"],
        population=planet_info["population"],
        films=planet_info["films"]
    )

    mocked_planets_service.get_planet_by_id.assert_called_once_with(
        id=planet_info["id"]
    )


def test_update_planet_must_call_update_planet_and_get_planet_by_id_from_service_when_scussess(
    mocked_planets_service,
    planet_info
):
    Planet.update_planet(
        id=planet_info["id"],
        name=planet_info["name"],
        climate=planet_info["climate"],
        diameter=planet_info["diameter"],
        population=planet_info["population"],
        films=planet_info["films"],
        using_service=mocked_planets_service
    )

    mocked_planets_service.update_planet.assert_called_once_with(
        id=planet_info["id"],
        name=planet_info["name"],
        climate=planet_info["climate"],
        diameter=planet_info["diameter"],
        population=planet_info["population"],
        films=planet_info["films"]
    )

    mocked_planets_service.get_planet_by_id.assert_called_once_with(
        id=planet_info["id"]
    )


def test_get_planet_must_return_object_when_receive_a_dict(
    planet_info
):
    planet = Planet.get_planet(planet_info)

    assert planet.id == planet_info["id"]
    assert planet.name == planet_info["name"]
    assert planet.climate == planet_info["climate"]
    assert planet.diameter == planet_info["diameter"]
    assert planet.population == planet_info["population"]
    assert planet.films == planet_info["films"]
    assert planet.created == planet_info["created"]
    assert planet.edited == planet_info["edited"]


def test_get_planet_must_return_none_when_receive_a_empty_dict():
    planet = Planet.get_planet({})

    assert planet is None


def test_get_planet_by_id_must_call_get_planet_by_id_from_service_and_return_a_planet_object(
    mocked_planets_service,
    planet_info
):
    planet = Planet.get_planet_by_id(
        id=planet_info["id"],
        using_service=mocked_planets_service
    )

    mocked_planets_service.get_planet_by_id.assert_called_once_with(
        id=planet_info["id"]
    )

    assert isinstance(planet, Planet)


def test_remove_planet_must_call_remove_planet_from_service(
    mocked_planets_service,
    planet_info
):
    Planet.remove_planet(
        id=planet_info["id"],
        using_service=mocked_planets_service
    )

    mocked_planets_service.remove_planet.assert_called_once_with(
        id=planet_info["id"]
    )
