from dataclasses import dataclass
from string import Template

from modules.core.manager import AirportManager


@dataclass
class FlightRoute:
    departure_airport_iata: str
    arrival_airport_iata: str
    airport_names: bool = False
    direction: str = 'forward'

    def __str__(self):
        route_string_template = Template("$departure $both-> $arrival")
        departure = self.departure_airport_iata
        arrival = self.arrival_airport_iata
        if self.airport_names:
            departure = AirportManager.build_airport_name(self.departure_airport_iata)
            arrival = AirportManager.build_airport_name(self.arrival_airport_iata)
        route_string = route_string_template.safe_substitute(
            departure=departure if self.direction == 'forward' else arrival,
            arrival=arrival if self.direction == 'forward' else departure,
            both='<' if self.direction == 'both' else ''
        )
        return route_string
