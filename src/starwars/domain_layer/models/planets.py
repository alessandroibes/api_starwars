from dataclasses import dataclass
from typing import List, Optional, Type

from starwars.domain_layer.ports.planets import PlanetsService


@dataclass
class Planet():
    id: str
    name: str
    climate: Optional[str]
    diameter: Optional[str]
    population: Optional[str]
    films: Optional[List[str]]
    created: Optional[str]
    edited: Optional[str]

    @classmethod
    def create_planet(
        cls,
        name: str,
        climate: Optional[str],
        diameter: Optional[str],
        population: Optional[str],
        films: List[str],
        using_service: Type[PlanetsService]
    ) -> "Planet":
        planet_data = {
            "name": name,
            "climate": climate,
            "diameter": diameter,
            "population": population,
            "films": films
        }

        planet_id = using_service.persist_planet(**planet_data)

        return cls.get_planet_by_id(
            id=planet_id,
            using_service=using_service
        )
    
    @classmethod
    def update_planet(
        cls,
        id: str,
        name: str,
        climate: Optional[str],
        diameter: Optional[str],
        population: Optional[str],
        films: List[str],
        using_service: Type[PlanetsService]
    ) -> "Planet":
        planet_data = {
            "id": id,
            "name": name,
            "climate": climate,
            "diameter": diameter,
            "population": population,
            "films": films
        }

        using_service.update_planet(**planet_data)

        return cls.get_planet_by_id(
            id=id,
            using_service=using_service
        )

    @classmethod
    def get_planet(
        cls,
        planet: dict
    ) -> "Planet":
        if planet:
            return cls(
                id=planet["id"],
                name=planet["name"],
                climate=planet.get("climate", None),
                diameter=planet.get("diameter", None),
                population=planet.get("population", None),
                films=planet.get("films", []),
                created=planet.get("created", None),
                edited=planet.get("edited", None)
            )
        
        return None

    @classmethod
    def get_planet_by_id(
        cls,
        id: str,
        using_service: Type[PlanetsService]
    ) -> Optional["Planet"]:
        planet = using_service.get_planet_by_id(id=id)

        return cls.get_planet(planet=planet)
    
    @classmethod
    def remove_planet(
        cls,
        id: str,
        using_service: Type[PlanetsService]
    ) -> None:
        using_service.remove_planet(id=id)
    
    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "population": self.population,
            "films": self.films,
            "created": self.created.isoformat(),
            "edited": self.edited.isoformat()
        }
