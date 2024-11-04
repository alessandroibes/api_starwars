from dataclasses import dataclass
from typing import List, Optional, Type

from starwars.domain_layer.ports.films import FilmsService


@dataclass
class Film:
    id: str
    title: str
    release_date: Optional[str]
    director: Optional[str]
    planets: Optional[List[str]]
    created: Optional[str]
    edited: Optional[str]

    @classmethod
    def create_film(
        cls,
        title: str,
        release_date: Optional[str],
        director: Optional[str],
        planets: List[str],
        using_service: Type[FilmsService]
    ) -> "Film":
        film_data = {
            "title": title,
            "release_date": release_date,
            "director": director,
            "planets": planets
        }

        film_id = using_service.persist_film(**film_data)

        return cls.get_film_by_id(
            id=film_id,
            using_service=using_service
        )
    
    @classmethod
    def update_film(
        cls,
        id: str,
        title: str,
        release_date: Optional[str],
        director: Optional[str],
        planets: List[str],
        using_service: Type[FilmsService]
    ) -> "Film":
        film_data = {
            "id": id,
            "title": title,
            "release_date": release_date,
            "director": director,
            "planets": planets
        }

        using_service.update_film(**film_data)

        return cls.get_film_by_id(
            id=id,
            using_service=using_service
        )
    
    @classmethod
    def get_film(
        cls,
        film: dict
    ) -> "Film":
        if film:
            return cls(
                id=film["id"],
                title=film["title"],
                release_date=film.get("release_date", None),
                director=film.get("director", None),
                planets=film.get("planets", []),
                created=film.get("created", None),
                edited=film.get("edited", None)
            )
        
        return None
    
    @classmethod
    def get_film_by_id(
        cls,
        id: str,
        using_service: Type[FilmsService]
    ) -> Optional["Film"]:
        film = using_service.get_film_by_id(id=id)

        return cls.get_film(film=film)

    @classmethod
    def remove_film(
        cls,
        id: str,
        using_service: Type[FilmsService]
    ) -> None:
        using_service.remove_film(id=id)

    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "director": self.director,
            "planets": self.planets,
            "created": self.created.isoformat(),
            "edited": self.edited.isoformat()
        }