from datetime import date
from string import Template
from typing import List

from modules.core.fetcher import FlightFetcher
from modules.entities.route import FlightRoute
from modules.entities.flight import FlightInfo


class FlightSchedule:

    def print(self):
        print(str(self))

    def __str__(self):
        result_schedule_str = ""
        schedule_header = Template("\t\t[Расписание рейсов $flight_direction на $flight_date]\t\t\n")
        result_schedule_str += schedule_header.safe_substitute(
            flight_direction=self.flight_direction,
            flight_date=self.flight_date
        )
        for flight in self._flights:
            result_schedule_str += str(flight) + '\n'

        return result_schedule_str

    @property
    def flights(self):
        flights = self._flights
        if self.direction == 'forward':
            flights = [f for f in flights
                       if f.departure_airport_iata == self.flight_direction.departure_airport_iata]
        if self.direction == 'backward':
            flights = [f for f in flights
                       if f.departure_airport_iata == self.flight_direction.arrival_airport_iata]
        return flights

    def __init__(self, flight_fetcher: FlightFetcher = None, direction: str = 'both'):
        self._flights: List[FlightInfo] = flight_fetcher.flights
        self.flight_direction: FlightRoute = flight_fetcher.flight_route
        self.direction: str = direction
        self.flight_date: date = flight_fetcher.flight_date
