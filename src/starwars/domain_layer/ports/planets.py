from abc import ABC
from typing import List

class DuplicatedPlanet(Exception):
    pass


class InvalidPlanet(Exception):
    pass


class PlanetsService(ABC):
    @classmethod
    def persist_planet(
        cls,
        name: str,
        climate: str,
        diameter: str,
        population: str,
        films: List[str]
    ):
        raise NotImplementedError
    
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
        raise NotImplementedError

    @classmethod
    def get_planet_by_id(cls, id: str):
        raise NotImplementedError
    
    @classmethod
    def remove_planet(cls, id: str):
        raise NotImplementedError