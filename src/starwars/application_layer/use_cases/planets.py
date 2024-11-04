from starwars.application_layer.adapters.planets_repository import PlanetsRepository
from starwars.domain_layer.models.planets import Planet
from starwars.domain_layer.ports.planets import DuplicatedPlanet
from starwars.presentation_layer.mappings import PlanetMapping


class PlanetAlreadyRegistered(Exception):
    pass


class PlanetsUseCase:

    @classmethod
    def create_planet(cls, data: "PlanetMapping"):
        try:
            planet = Planet.create_planet(
                name=data.name,
                climate=data.climate,
                diameter=data.diameter,
                population=data.population,
                films=data.films,
                using_service=PlanetsRepository
            )

            return planet.as_dict()
        except DuplicatedPlanet:
            raise PlanetAlreadyRegistered(f"Planet with name {data.name} already exists")
        
    @classmethod
    def update_planet(cls, id: str, data: "PlanetMapping"):
        try:
            planet = Planet.update_planet(
                id=id,
                name=data.name,
                climate=data.climate,
                diameter=data.diameter,
                population=data.population,
                films=data.films,
                using_service=PlanetsRepository
            )

            return planet.as_dict()
        except DuplicatedPlanet:
            raise PlanetAlreadyRegistered(f"Planet with name {data.name} already exists")
    
    @classmethod
    def remove_planet(cls, id: str):
        Planet.remove_planet(
            id=id,
            using_service=PlanetsRepository
        )

    @classmethod
    def get_planet_by_id(cls, id: str):
        planet = Planet.get_planet_by_id(
            id,
            using_service=PlanetsRepository
        )

        if planet:
            return planet.as_dict()