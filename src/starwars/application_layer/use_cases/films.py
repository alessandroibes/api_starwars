from starwars.application_layer.adapters.films_repository import FilmsRepository
from starwars.domain_layer.models.films import Film
from starwars.domain_layer.ports.films import DuplicatedFilm
from starwars.presentation_layer.mappings import FilmMapping


class FilmAlreadyRegistered(Exception):
    pass


class FilmsUseCase:

    @classmethod
    def create_film(cls, data: "FilmMapping"):
        try:
            film = Film.create_film(
                title=data.title,
                release_date=data.release_date,
                director=data.director,
                planets=data.planets,
                using_service=FilmsRepository
            )

            return film.as_dict()
        except DuplicatedFilm:
            raise FilmAlreadyRegistered(f"Film with title {data.title} already exists")
        
    @classmethod
    def update_film(cls, id: str, data: "FilmMapping"):
        try:
            film = Film.update_film(
                id=id,
                title=data.title,
                release_date=data.release_date,
                director=data.director,
                planets=data.planets,
                using_service=FilmsRepository
            )

            return film.as_dict()
        except DuplicatedFilm:
            raise FilmAlreadyRegistered(f"Film with title {data.title} already exists")
    
    @classmethod
    def remove_film(cls, id: str):
        Film.remove_film(
            id=id,
            using_service=FilmsRepository
        )
        
    @classmethod
    def get_film_by_id(cls, id: str):
        film = Film.get_film_by_id(
            id,
            using_service=FilmsRepository
        )

        if film:
            return film.as_dict()