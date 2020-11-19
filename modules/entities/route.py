from dataclasses import dataclass


@dataclass
class FlightRoute:
    departure_airport_iata: str
    arrival_airport_iata: str

    def __str__(self):
        return "{} -> {}".format(self.departure_airport_iata, self.arrival_airport_iata)
