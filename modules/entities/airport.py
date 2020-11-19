from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class Airport(BaseModel):
    name: str
    iata: str
    city: str = ''
    country: str = ''
    icao: str = ''

    def __str__(self):
        airport_name = "{name}, {city} ({country})"
        return airport_name.format(
            name=self.name,
            city=self.city,
            country=self.country
        )
