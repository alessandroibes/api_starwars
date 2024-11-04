from typing import List, Optional


class PayloadMapping:
    def __init__(self, *, payload):
        self.payload = payload


class FilmMapping(PayloadMapping):
    @property
    def title(self) -> str:
        return self.payload["title"]
    
    @property
    def release_date(self) -> Optional[str]:
        return self.payload.get("release_date", None)
    
    @property
    def director(self) -> Optional[str]:
        return self.payload.get("director", None)
    
    @property
    def planets(self) -> Optional[List[str]]:
        return self.payload.get("planets", [])


class PlanetMapping(PayloadMapping):
    @property
    def name(self) -> str:
        return self.payload["name"]
    
    @property
    def climate(self) -> Optional[str]:
        return self.payload.get("climate", None)
    

    @property
    def diameter(self) -> Optional[str]:
        return self.payload.get("diameter", None)
    
    @property
    def population(self) -> Optional[str]:
        return self.payload.get("population", None)
    
    @property
    def films(self) -> Optional[List[str]]:
        return self.payload.get("films", [])
