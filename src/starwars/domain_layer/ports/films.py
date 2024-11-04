from abc import ABC
from typing import List


class DuplicatedFilm(Exception):
    pass


class InvalidFilm(Exception):
    pass


class FilmsService(ABC):
    @classmethod
    def persist_film(
        cls,
        title: str,
        release_date: str,
        director: str,
        planets: List[str]
    ):
        raise NotImplementedError
    
    @classmethod
    def update_film(
        cls,
        id: str,
        title: str,
        release_date: str,
        director: str,
        planets: List[str]
    ):
        raise NotImplementedError
    
    @classmethod
    def get_film_by_id(cls, id: str):
        raise NotImplementedError
    
    @classmethod
    def remove_film(cls, id: str):
        raise NotImplementedError